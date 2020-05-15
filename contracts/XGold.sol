pragma solidity 0.5.12;

import './library/ERC20SafeTransfer';
import './library/Pausable';
import './library/SafeMath';

contract XGold is Pausable, ERC20SafeTransfer {
    using SafeMath for uint;
    // --- Data ---
    bool private initialized;     // flag of initialize data

    address public token;

    uint public exchangeRate = 31103500000000000000;     // the rate accumulator
    uint constant ONE = 10 ** 18;

    // --- ERC20 Data ---
    string  public name;
    string  public symbol;
    uint8   public decimals;
    uint256 public totalSupply;

    mapping (address => uint)                      public balanceOf;
    mapping (address => mapping (address => uint)) public allowance;

    // --- Event ---
    event Approval(address indexed src, address indexed guy, uint wad);
    event Transfer(address indexed src, address indexed dst, uint wad);
    
    /**
     * The constructor is used here to ensure that the implementation
     * contract is initialized. An uncontrolled implementation
     * contract might lead to misleading state
     * for users who accidentally interact with it.
     */
    constructor(string memory _name, string memory _symbol, address _token) public {
        initialize(_name, _symbol, _token);
    }

    // --- Init ---
    // Do not modify this function
    function initialize(string memory _name, string memory _symbol, address _token) public {
        require(!initialized, "initialize: already initialized.");
        name = _name;
        symbol = _symbol;
        token = _token;
        decimals = uint8(IERC20(_token).decimals());
        owner = msg.sender;
        initialized = true;
    }

    // --- Math ---
    function rmul(uint x, uint y) internal pure returns (uint z) {
        z = x.mul(y) / ONE;
    }

    function rdiv(uint x, uint y) internal pure returns (uint z) {
        z = x.mul(ONE) / y;
    }

    /**
     * @dev Deposit token to earn savings, but only when the contract is not paused.
     * @param _dst account who will get benefits.
     * @param _pie amount to buy, scaled by 1e18.
     */
    function mint(address _dst, uint _pie) external whenNotPaused {
        require(doTransferFrom(token, msg.sender, address(this), _pie));
        uint _wad = rmul(_pie, exchangeRate);
        balanceOf[_dst] = balanceOf[_dst].add(_wad);
        totalSupply = totalSupply.add(_wad);
        emit Transfer(address(0), _dst, _wad);
    }

    /**
     * @dev Withdraw to get token according to input xGold amount, but only when the contract is not paused.
     * @param _src account who will receive benefits.
     * @param _wad amount to burn xGold, scaled by 1e18.
     */
    function burn(address _src, uint _wad) external whenNotPaused {
        require(balanceOf[_src] >= _wad, "exit: insufficient balance");
        if (_src != msg.sender && allowance[_src][msg.sender] != uint(-1)) {
            require(allowance[_src][msg.sender] >= _wad, "exit: insufficient allowance");
            allowance[_src][msg.sender] = allowance[_src][msg.sender].sub(_wad);
        }
        balanceOf[_src] = balanceOf[_src].sub(_wad);
        totalSupply = totalSupply.sub(_wad);

        require(doTransferOut(token, msg.sender, rdiv(_wad, exchangeRate)));
        emit Transfer(_src, address(0), _wad);
    }

    /**
     * @dev Withdraw to get specified token, but only when the contract is not paused.
     * @param _src account who will receive benefits.
     * @param _pie amount to redeem token, scaled by 1e18.
     */
    function redeem(address _src, uint _pie) external whenNotPaused {
        require(getTokenBalance(_src) >= _pie, "redeem: insufficient token balance");
        uint _wad = rmul(_pie, exchangeRate);
        require(balanceOf[_src] >= _wad, "redeem: insufficient balance");
        if (_src != msg.sender && allowance[_src][msg.sender] != uint(-1)) {
            require(allowance[_src][msg.sender] >= _wad, "redeem: insufficient allowance");
            allowance[_src][msg.sender] = allowance[_src][msg.sender].sub(_wad);
        }
        balanceOf[_src] = balanceOf[_src].sub(_wad);
        totalSupply = totalSupply.sub(_wad);

        require(doTransferOut(token, msg.sender, _pie));
        emit Transfer(_src, address(0), _wad);
    }

    // --- ERC20 ---
    function transfer(address _dst, uint _wad) external returns (bool) {
        return transferFrom(msg.sender, _dst, _wad);
    }

    function transferFrom(address _src, address _dst, uint _wad) public returns (bool) {
        require(balanceOf[_src] >= _wad, "transferFrom: insufficient balance");
        if (_src != msg.sender && allowance[_src][msg.sender] != uint(-1)) {
            require(allowance[_src][msg.sender] >= _wad, "transferFrom: insufficient allowance");
            allowance[_src][msg.sender] = allowance[_src][msg.sender].sub(_wad);
        }
        balanceOf[_src] = balanceOf[_src].sub(_wad);
        balanceOf[_dst] = balanceOf[_dst].add(_wad);
        emit Transfer(_src, _dst, _wad);
        return true;
    }

    function approve(address _spender, uint _wad) external returns (bool) {
        allowance[msg.sender][_spender] = _wad;
        emit Approval(msg.sender, _spender, _wad);
        return true;
    }

    /**
     * @dev Total amount with earning savings.
     * @param _src account to query current total balance.
     * @return total balance with any accumulated interest.
     */
    function getTokenBalance(address _src) public view returns (uint) {
        return getRedeemAmount(balanceOf[_src]);
    }

    /**
     * @dev Total amount with earning savings.
     * @param _wad amount of xGold, scaled by 1e18.
     * @return amount of token, scaled by 1e18.
     */
    function getRedeemAmount(uint _wad) public view returns (uint) {
        return rdiv(_wad, exchangeRate);
    }
}
