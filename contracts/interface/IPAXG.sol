pragma solidity 0.5.16;

interface IPAXG {
    function feeParts() external view returns (uint256);
    function feeRate() external view returns (uint256);
}
