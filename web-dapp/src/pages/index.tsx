import React from 'react';
import styles from './index.less';
import './reset.less';
import '../cssdir/foot.less';
import '../cssdir/header.less';
import tips from '../cssdir/tips.less';
import 'antd/dist/antd.css';
import { Tabs, Button, Input, Dropdown, Menu, Modal } from 'antd';
import { IntlProvider, FormattedMessage } from 'react-intl';
import en_US from '../language/en_US.js';
import zh_CN from '../language/zh_CN.js';
import History from '../history/history.js';
import Web3 from 'web3';
import {
  get_nettype,
  init_contract,
  check_approve,
  get_my_account,
  get_my_balance,
  get_my_eth,
  format_bn,
  format_num_to_K,
  paxg_change,
  get_totalSupply,
  get_balanceOf,
  click_mint,
  getBaseData,
  goldx_change,
  click_redeem,
  paxg_click_max,
  goldx_click_max,
  calc_rate,
  calc_rate_plus
} from '../utils.js';
import logo_goldx from '../images/logo_goldx.svg';
import logo_paxg from '../images/logo_paxg.svg';
import icon_arrow from '../images/icon_arrow.svg';
import Twitter from '../images/twitter.svg';
import Telegram from '../images/telegram.svg';
import Medium from '../images/medium.svg';
import Reddit from '../images/Reddit.svg';
import Discord from '../images/Discord.svg';
import LinkedIn from '../images/LinkedIn.svg';
import Youtube from '../images/Youtube.svg';
import erweima from '../images/erweima.png';
import weixin from '../images/weixin.svg';
import arrow_u from '../images/up.svg';
import logo_goldx_log from '../images/logo-goldx.svg';
import arrow_d from '../images/arrow_d.svg';
import wallet_metamask from '../images/wallet-metamask.svg';
import isMobile from 'is-mobile';
import close_new from '../images/close-new.svg';
import close from '../images/close.svg';
import no_support from '../images/no_support.svg';
import img_is_open from '../images/img_is_open.svg';

const { TabPane } = Tabs;

declare global {
  interface Window {
    ethereum: any
  }
}

export default class Index extends React.Component<any, any> {
  new_web3: Web3;
  bn: any;

  constructor(props: any) {
    super(props);

    this.state = {
      cur_language: navigator.language === 'zh-CN' ? '中文' : 'English',
      is_already: false,
      meun1: true,
      meun2: true,
      meun3: true,
      show_pause: false,
    }

    this.new_web3 = new Web3(Web3.givenProvider || null);
    this.bn = this.new_web3.utils.toBN;
  }

  init_metamask_wallet = async () => {
    this.setState({
      show_wallets: false
    })

    let nettype,
      contract_GOLDx,
      contract_PAXG,
      my_account,
      is_approve,
      my_balance_paxg,
      my_balance_goldx,
      my_balance_eth,
      totalSupply_paxg,
      totalSupply_goldx,
      balanceOf_paxg,
      show_pause,
      BaseData;


    try {
      nettype = await get_nettype(this.new_web3);
      this.setState({
        net_type: nettype,
      })

      contract_GOLDx = await init_contract(this.new_web3, nettype, 'GOLDx');
      contract_PAXG = await init_contract(this.new_web3, nettype, 'PAXG');

      my_account = await get_my_account(this.new_web3);
      is_approve = await check_approve(contract_PAXG, my_account, nettype);

      my_balance_paxg = await get_my_balance(contract_PAXG, my_account, nettype);
      my_balance_goldx = await get_my_balance(contract_GOLDx, my_account, nettype);
      my_balance_eth = await get_my_eth(this.new_web3, my_account);

      totalSupply_paxg = await get_totalSupply(contract_PAXG);
      totalSupply_goldx = await get_totalSupply(contract_GOLDx);
      balanceOf_paxg = await get_balanceOf(contract_PAXG, nettype);

      BaseData = await getBaseData(contract_GOLDx);
      show_pause = BaseData[7];

      this.setState({
        load_new_history: Math.random(),
        is_already: true,
        contract_GOLDx: contract_GOLDx,
        contract_PAXG: contract_PAXG,
        my_account: my_account,
        is_approve: this.bn(is_approve).gt(this.bn(0)),
        my_balance_paxg: my_balance_paxg,
        my_balance_goldx: my_balance_goldx,
        my_balance_eth: my_balance_eth,
        totalSupply_paxg: totalSupply_paxg,
        totalSupply_goldx: totalSupply_goldx,
        balanceOf_paxg: balanceOf_paxg,
        BaseData: BaseData,
        show_pause
      }, () => {
        calc_rate(this);
        calc_rate_plus(this);
      })

      let wallet_type = JSON.parse(`${window.localStorage.getItem('wallet_type')}`) || {};
      console.log(wallet_type);
      wallet_type.wallet_type = 'metamask';
      window.localStorage.setItem('wallet_type', JSON.stringify(wallet_type));
    } catch (error) {
      console.log(error)
    }
  }



  click_wallet = (walletType: any) => {
    // console.log(Web3.givenProvider);
    // return;
    if (!Web3.givenProvider) {
      return false;
    }

    let wallet_type_first = JSON.parse(`${window.localStorage.getItem('wallet_type')}`) || {};
    console.log(wallet_type_first);
    if (wallet_type_first.wallet_type === walletType) {
      this.setState({
        show_wallets: false
      })
      return console.log('aready connect metamask');
    }

    this.init_metamask_wallet();
  }

  componentDidMount = () => {
    if (!Web3.givenProvider) {
      return console.log('no web3 provider');
    }

    if (isMobile()) {
      this.setState({
        show_wallets: false
      })

      this.init_metamask_wallet();

      let g_timer = setInterval(async () => {
        if (this.state.my_account && this.state.contract_GOLDx && this.state.contract_PAXG) {
          let is_approve = await check_approve(this.state.contract_PAXG, this.state.my_account, this.state.net_type);
          let my_balance_paxg = await get_my_balance(this.state.contract_PAXG, this.state.my_account, this.state.net_type);
          let my_balance_goldx = await get_my_balance(this.state.contract_GOLDx, this.state.my_account, this.state.net_type);
          let my_balance_eth = await get_my_eth(this.new_web3, this.state.my_account);
          let totalSupply_paxg = await get_totalSupply(this.state.contract_PAXG);
          let totalSupply_goldx = await get_totalSupply(this.state.contract_GOLDx);
          let balanceOf_paxg = await get_balanceOf(this.state.contract_PAXG, this.state.net_type);
          let BaseData = await getBaseData(this.state.contract_GOLDx);
          let show_pause = BaseData[7];
          this.setState({
            is_already: true,
            is_approve: this.bn(is_approve).gt(this.bn(0)),
            my_balance_paxg: my_balance_paxg,
            my_balance_goldx: my_balance_goldx,
            my_balance_eth: my_balance_eth,
            totalSupply_paxg: totalSupply_paxg,
            totalSupply_goldx: totalSupply_goldx,
            balanceOf_paxg: balanceOf_paxg,
            BaseData: BaseData,
            show_pause: show_pause
          }, () => {
            calc_rate(this);
            calc_rate_plus(this);
          })
        }
      }, 1000 * 5)

      return false;
    }


    if (window.localStorage) {
      let wallet_type = JSON.parse(`${window.localStorage.getItem('wallet_type')}`) || {};
      console.log(wallet_type);
      if (!wallet_type.wallet_type) {
        console.log('no wallet_type.wallet_type');
        this.setState({
          show_wallets: true
        })
      } else {
        if (wallet_type.wallet_type === 'metamask') {
          this.init_metamask_wallet();

          let g_timer = setInterval(async () => {
            if (this.state.my_account && this.state.contract_GOLDx && this.state.contract_PAXG) {
              let is_approve = await check_approve(this.state.contract_PAXG, this.state.my_account, this.state.net_type);
              let my_balance_paxg = await get_my_balance(this.state.contract_PAXG, this.state.my_account, this.state.net_type);
              let my_balance_goldx = await get_my_balance(this.state.contract_GOLDx, this.state.my_account, this.state.net_type);
              let my_balance_eth = await get_my_eth(this.new_web3, this.state.my_account);
              let totalSupply_paxg = await get_totalSupply(this.state.contract_PAXG);
              let totalSupply_goldx = await get_totalSupply(this.state.contract_GOLDx);
              let balanceOf_paxg = await get_balanceOf(this.state.contract_PAXG, this.state.net_type);
              let BaseData = await getBaseData(this.state.contract_GOLDx);
              let show_pause = BaseData[7];
              this.setState({
                is_already: true,
                is_approve: this.bn(is_approve).gt(this.bn(0)),
                my_balance_paxg: my_balance_paxg,
                my_balance_goldx: my_balance_goldx,
                my_balance_eth: my_balance_eth,
                totalSupply_paxg: totalSupply_paxg,
                totalSupply_goldx: totalSupply_goldx,
                balanceOf_paxg: balanceOf_paxg,
                BaseData: BaseData,
                show_pause
              })
            }
          }, 1000 * 5)
        }
      }
    }

    // add accounts changed
    if (window.ethereum && window.ethereum.on) {
      window.ethereum.on('accountsChanged', async (accounts: any[]) => {
        let my_account = accounts[0];
        this.setState({
          my_account: my_account,
          show_wallets: false
        }, async () => {
          let is_approve = await check_approve(this.state.contract_PAXG, this.state.my_account, this.state.net_type);
          let my_balance_paxg = await get_my_balance(this.state.contract_PAXG, this.state.my_account, this.state.net_type);
          let my_balance_goldx = await get_my_balance(this.state.contract_GOLDx, this.state.my_account, this.state.net_type);
          let my_balance_eth = await get_my_eth(this.new_web3, this.state.my_account);
          let totalSupply_paxg = await get_totalSupply(this.state.contract_PAXG);
          let totalSupply_goldx = await get_totalSupply(this.state.contract_GOLDx);
          let balanceOf_paxg = await get_balanceOf(this.state.contract_PAXG, this.state.net_type);
          let BaseData = await getBaseData(this.state.contract_GOLDx);
          let show_pause = BaseData[7];
          this.setState({
            is_already: true,
            is_approve: this.bn(is_approve).gt(this.bn(0)),
            my_balance_paxg: my_balance_paxg,
            my_balance_goldx: my_balance_goldx,
            my_balance_eth: my_balance_eth,
            totalSupply_paxg: totalSupply_paxg,
            totalSupply_goldx: totalSupply_goldx,
            balanceOf_paxg: balanceOf_paxg,
            BaseData: BaseData,
            show_pause
          })
        })
      })
    }
  }

  render() {
    return (
      <IntlProvider locale={'en'} messages={this.state.cur_language === '中文' ? zh_CN : en_US} >

        <Modal
          visible={this.state.show_wallets}
          onCancel={() => { this.setState({ show_wallets: false }) }}
          footer={false}
        >
          <div className={tips.title}>Connect Wallet</div>
          <div className={tips.wallets}>
            <div className={tips.wallets__item} onClick={() => { this.click_wallet('metamask') }}>
              <span className={tips.wallets__item_name}>{'MetaMask'}</span>
              <span className={tips.wallets__item_icon}>
                <img src={wallet_metamask} alt="" />
              </span>
            </div>
          </div>
        </Modal>

        {/* pause */}
        <Modal
          visible={this.state.show_pause}
          // onCancel={() => { this.setState({ show_pause: false }) }}
          footer={false}
          closable={false}
          maskClosable={false}
        >
          <div className='popup-is-open'>
            <img src={img_is_open} alt='' />
            <div className='popup-is-open-text'>System Maintain, Come back Soon...</div>
            <div className='popup-is-open-text'>系统维护，敬请期待...</div>
          </div>
        </Modal>


        {/* *** *** *** *** *** *** mobile *** *** *** *** *** *** */}
        <div className='wrap-mob'>
          <div className='only-left'>
            <a href="https://goldx.dforce.network" className={'header__logo'}>
              <img src={logo_goldx_log} alt="logo" />
            </a>
          </div>
          <div className='only-right'>
            <img src={close} alt='' onClick={() => { this.setState({ showonly: true }) }} />
          </div>
          <div className='clear'></div>
        </div>

        <div className={this.state.showonly ? 'mobile-only' : 'disn'}>
          <div className='wrap-mob'>
            <div className='only-left'>
              <a href="https://goldx.dforce.network" className={'header__logo'}>
                <img src={logo_goldx_log} alt="logo" />
              </a>
            </div>
            <div className='only-right'>
              <img src={close_new} alt='' onClick={() => { this.setState({ showonly: false }) }} />
            </div>
            <div className='clear'></div>
          </div>
          <div className='only-kong'></div>

          <h1 onClick={() => { this.setState({ meun1: !this.state.meun1 }) }}>
            <FormattedMessage id='dForce_Stablecoin' />
            <span>
              <img src={this.state.meun1 ? arrow_u : arrow_d} />
            </span>
          </h1>
          <div className={this.state.meun1 ? 'meun1' : 'only1px'}>
            <div className='m-item'>
              <a href='https://usdx.dforce.network/' target='_blank' rel="noopener noreferrer">
                <span className='title'>USDx</span>
              </a>
              <span className='details'><FormattedMessage id='Portal' /></span>
            </div>

            <div className='m-item'>
              <a href='https://usr.dforce.network/' target='_blank' rel="noopener noreferrer">
                <span className='title'>USR</span>
              </a>
              <span className='details'><FormattedMessage id='usr_content' /></span>
            </div>

            <div className='m-item'>
              <a href='https://markets.dforce.network/' target='_blank' rel="noopener noreferrer">
                <span className='title'>
                  <FormattedMessage id='Yield_Markets' />
                </span>
              </a>
              <span className='details'>
                <FormattedMessage id='Yield_Markets_detail' />
              </span>
            </div>
            <div className='m-item'>
              <a href='https://goldx.dforce.network/' target='_blank' rel="noopener noreferrer">
                <span className='title'>
                  <FormattedMessage id='goldx' />
                </span>
              </a>
              <span className='details'>
                <FormattedMessage id='goldx_detail' />
              </span>
            </div>
          </div>

          <h1 onClick={() => { this.setState({ meun2: !this.state.meun2 }) }}>
            <FormattedMessage id='Exchange_Market' />
            <span>
              <img src={this.state.meun2 ? arrow_u : arrow_d} />
            </span>
          </h1>
          <div className={this.state.meun2 ? 'meun1' : 'only1px'}>
            <div className='m-item'>
              <a href='https://trade.dforce.network/' target='_blank' rel="noopener noreferrer">
                <span className='title'>dForce Trade</span>
              </a>
              <span className='details'><FormattedMessage id='Instant_Swap_of_Stable_Assets' /></span>
            </div>
          </div>

          <h1 onClick={() => { this.setState({ meun3: !this.state.meun3 }) }}>
            <FormattedMessage id='Governance' />
            <span>
              <img src={this.state.meun3 ? arrow_u : arrow_d} />
            </span>
          </h1>
          <div className={this.state.meun3 ? 'meun1' : 'only1px'}>
            <div className='m-item'>
              <a href='https://airdrop.dforce.network/' rel="noopener noreferrer">
                <span className='title'>Airdrop</span>
              </a>
              <span className='details'>
                <FormattedMessage id='DF_token_distribute_system' />
              </span>
            </div>
          </div>

        </div>
        {/* *** *** *** *** *** *** mobile *** *** *** *** *** *** */}


        <div className={'header'}>
          <a href="https://goldx.dforce.network" className={'header__logo'}>
            <img src={logo_goldx_log} alt="logo" />
          </a>

          <div className={'header__menu'}>
            <Dropdown
              overlay={
                <Menu className={'header__overlay'}>
                  <Menu.Item>
                    <a target="_blank" rel="noopener noreferrer" href="https://usdx.dforce.network/" className={'header__overlay_item'}>
                      <span>USDx</span>
                      <label>
                        <FormattedMessage id='Portal' />
                      </label>
                    </a>
                  </Menu.Item>

                  <Menu.Item>
                    <a target="_blank" rel="noopener noreferrer" href="https://usr.dforce.network/" className={'header__overlay_item'}>
                      <span>USR</span>
                      <label>
                        <FormattedMessage id='usr_content' />
                      </label>
                    </a>
                  </Menu.Item>

                  <Menu.Item>
                    <a target="_blank" rel="noopener noreferrer" href="https://markets.dforce.network/" className={'header__overlay_item'}>
                      <span>
                        <FormattedMessage id='Yield_Markets' />
                      </span>
                      <label>
                        <FormattedMessage id='Yield_Markets_detail' />
                      </label>
                    </a>
                  </Menu.Item>
                  <Menu.Item>
                    <a target="_blank" rel="noopener noreferrer" href="https://goldx.dforce.network/" className={'header__overlay_item'}>
                      <span>
                        <FormattedMessage id='goldx' />
                      </span>
                      <label>
                        <FormattedMessage id='goldx_detail' />
                      </label>
                    </a>
                  </Menu.Item>
                </Menu>
              }
            >
              <span className={'header__menu_item'}>
                <label><FormattedMessage id='dForce_Stablecoin' /></label>
                <img src={arrow_d} alt="down" />
              </span>
            </Dropdown>


            <Dropdown
              overlay={
                <Menu className={'header__overlay'}>
                  <Menu.Item>
                    <a rel="noopener noreferrer" href="https://trade.dforce.network/" className={'header__overlay_item'}>
                      <span>dForce Trade</span>
                      <label>
                        <FormattedMessage id='Instant_Swap_of_Stable_Assets' />
                      </label>
                    </a>
                  </Menu.Item>
                </Menu>
              }
            >
              <span className={'header__menu_item'}>
                <label>
                  <FormattedMessage id='Exchange_Market' />
                </label>
                <img src={arrow_d} alt="down" />
              </span>
            </Dropdown>


            <Dropdown
              overlay={
                <Menu className={'header__overlay'}>
                  <Menu.Item>
                    <a rel="noopener noreferrer" href="https://airdrop.dforce.network/" className={'header__overlay_item'}>
                      <span>Airdrop</span>
                      <label>
                        <FormattedMessage id='DF_token_distribute_system' />
                      </label>
                    </a>
                  </Menu.Item>
                </Menu>
              }
            >
              <span className={'header__menu_item'}>
                <label>
                  <FormattedMessage id='Governance' />
                </label>
                <img src={arrow_d} alt="down" />
              </span>
            </Dropdown>


            {
              this.state.net_type && (this.state.net_type === 'rinkeby' || this.state.net_type === 'main') &&
              <>
                {
                  this.state.my_account &&
                  <a
                    className={'header__menu_wallet'} target="_blank"
                    href={
                      this.state.net_type !== 'rinkeby'
                        ? `https://etherscan.com/address/${this.state.my_account}`
                        : `https://rinkeby.etherscan.io/address/${this.state.my_account}`
                    }
                  >
                    <div>
                      <i style={{ backgroundColor: this.state.net_type !== 'rinkeby' ? '#29B6AF' : '#e2bc73' }}></i>
                      {this.state.my_account.slice(0, 4) + '...' + this.state.my_account.slice(-4)}
                    </div>
                  </a>
                }
                {
                  !this.state.my_account &&
                  <a className={'header__menu_wallet'} onClick={() => { this.setState({ show_wallets: true }) }}>
                    <FormattedMessage id='connect' />
                  </a>
                }
              </>
            }
            {
              this.state.net_type && !(this.state.net_type === 'rinkeby' || this.state.net_type === 'main') &&
              <a className={'header__menu_wallet header__menu_wallet_notsup'} href='javascript:;'>
                <img src={no_support} alt='' />
                <span>Wrong Network</span>
              </a>
            }
          </div>
        </div>


        <div className={styles.content}>
          <div className={styles.content_top_mobile}>
            <div className={styles.balance_mobile}>
              <span className={styles.balance_left}>
                <FormattedMessage id='Goldx_Outstanding' />
              </span>
              <span className={styles.balance_right}>
                {this.state.totalSupply_goldx ? format_num_to_K(format_bn(this.state.totalSupply_goldx, 18, 2)) : '...'}
              </span>
            </div>
            <div className={styles.balance_mobile}>
              <span className={styles.balance_left}>
                <FormattedMessage id='PAXG_Total_Supply' />
              </span>
              <span className={styles.balance_right}>
                {this.state.totalSupply_paxg ? format_num_to_K(format_bn(this.state.totalSupply_paxg, 18, 2)) : '...'}
              </span>
            </div>
            <div className={styles.balance_mobile}>
              <span className={styles.balance_left}>
                <FormattedMessage id='Total_PAXG_in_Goldx' />
              </span>
              <span className={styles.balance_right}>
                {this.state.balanceOf_paxg ? format_num_to_K(format_bn(this.state.balanceOf_paxg, 18, 2)) : '...'}
              </span>
            </div>
          </div>

          <div className={styles.content_left}>
            <div className={styles.content_left_top}>
              <Tabs
                tabBarStyle={{ fontSize: '16px', fontWeight: 'bold' }}
              >
                <TabPane tab={this.state.cur_language === '中文' ? "存入" : "MINT"} key="1">
                  <div className={styles.pane_top}>

                    <div className={styles.sec1}>
                      <div className={styles.sec1_token}>
                        <img src={logo_paxg} alt="" />
                        <span className={styles.span_token}>PAXG</span>
                        <span className={styles.mobile_balance}>
                          <FormattedMessage id='balance' />
                          <span className={styles.mobile_balance_num}>
                            {this.state.my_balance_paxg ? format_num_to_K(format_bn(this.state.my_balance_paxg, 18, 2)) : '...'}
                          </span>
                        </span>
                      </div>

                      <div className={styles.sec1_input}>
                        <Input
                          placeholder={'Amount in PAXG'}
                          type="text"
                          value={this.state.value_paxg}
                          onChange={(e) => { paxg_change(this, e.target.value) }}
                        />
                        <span className={styles.span_max} onClick={(e) => { paxg_click_max(this) }}>
                          MAX
                        </span>
                      </div>

                      <div className={styles.sec1_rate}>
                        1 PAXG = {this.state.paxg_to_goldx ? format_bn(this.state.paxg_to_goldx, 18, 6) : '...'} GOLDx
                      </div>
                    </div>

                    <div className={styles.sec2}>
                      <img src={icon_arrow} alt="" />
                    </div>

                    <div className={styles.sec1}>
                      <div className={styles.sec1_token}>
                        <img src={logo_goldx} alt="" />
                        <span className={styles.span_token}>GOLDx</span>
                        <span className={styles.mobile_balance}>
                          <FormattedMessage id='balance' />
                          <span className={styles.mobile_balance_num}>
                            {this.state.my_balance_goldx ? format_num_to_K(format_bn(this.state.my_balance_goldx, 18, 2)) : '...'}
                          </span>
                        </span>
                      </div>
                      <div className={styles.sec1_input}>
                        <Input type="text" disabled={true} value={this.state.to_receive_goldx} placeholder='0.00' />
                      </div>
                    </div>

                  </div>
                  <div className={styles.pane_bottom}>
                    <Button
                      onClick={() => { click_mint(this) }}
                      disabled={this.state.is_btn_disabled_mint}
                      className={this.state.is_btn_disabled_mint ? styles.btn_disabled : ''}
                    >
                      MINT
                    </Button>
                  </div>
                </TabPane>

                <TabPane tab={this.state.cur_language === '中文' ? "取回" : "REDEEM"} key="2">
                  <div className={styles.pane_top}>

                    <div className={styles.sec1}>
                      <div className={styles.sec1_token}>
                        <img src={logo_goldx} alt="" />
                        <span className={styles.span_token}>GOLDx</span>
                        <span className={styles.mobile_balance}>
                          <FormattedMessage id='balance' />
                          <span className={styles.mobile_balance_num}>
                            {this.state.my_balance_goldx ? format_num_to_K(format_bn(this.state.my_balance_goldx, 18, 2)) : '...'}
                          </span>
                        </span>
                      </div>

                      <div className={styles.sec1_input}>
                        <Input
                          placeholder={'Amount in GOLDx'}
                          type="text"
                          value={this.state.value_goldx}
                          onChange={(e) => { goldx_change(this, e.target.value) }}
                        />
                        <span className={styles.span_max} onClick={(e) => { goldx_click_max(this) }}>
                          MAX
                        </span>
                      </div>

                      <div className={styles.sec1_rate}>
                        1 GOLDx = {this.state.goldx_to_paxg ? format_bn(this.state.goldx_to_paxg, 18, 6) : '...'} PAXG
                      </div>
                    </div>

                    <div className={styles.sec2}>
                      <img src={icon_arrow} alt="" />
                    </div>

                    <div className={styles.sec1}>
                      <div className={styles.sec1_token}>
                        <img src={logo_paxg} alt="" />
                        <span className={styles.span_token}>PAXG</span>
                        <span className={styles.mobile_balance}>
                          <FormattedMessage id='balance' />
                          <span className={styles.mobile_balance_num}>
                            {this.state.my_balance_paxg ? format_num_to_K(format_bn(this.state.my_balance_paxg, 18, 2)) : '...'}
                          </span>
                        </span>
                      </div>
                      <div className={styles.sec1_input}>
                        <Input type="text" disabled={true} value={this.state.to_receive_paxg} placeholder='0.00' />
                      </div>
                    </div>

                  </div>
                  <div className={styles.pane_bottom}>
                    <Button
                      onClick={() => { click_redeem(this) }}
                      disabled={this.state.is_btn_disabled_redeem}
                      className={this.state.is_btn_disabled_redeem ? styles.btn_disabled : ''}
                    >
                      REDEEM
                    </Button>
                  </div>
                </TabPane>
              </Tabs>
            </div>
            <div className={styles.content_left_bottom}>
              <History
                account={this.state.my_account}
                net_type={this.state.net_type}
                new_web3={this.new_web3}
                load_new_history={this.state.load_new_history}
                cur_language={this.state.cur_language}
              />
            </div>
          </div>
          <div className={styles.content_right}>
            <div className={styles.title}>
              <FormattedMessage id='Wallet_Balance' />
            </div>
            <div className={styles.balance}>
              <span className={styles.balance_left}>ETH</span>
              <span className={styles.balance_right}>
                {this.state.my_balance_eth ? format_num_to_K(format_bn(this.state.my_balance_eth, 18, 2)) : '...'}
              </span>
            </div>

            <div className={styles.balance}>
              <span className={styles.balance_left}>GOLDx</span>
              <span className={styles.balance_right}>
                {this.state.my_balance_goldx ? format_num_to_K(format_bn(this.state.my_balance_goldx, 18, 2)) : '...'}
              </span>
            </div>

            <div className={styles.balance}>
              <span className={styles.balance_left}>PAXG</span>
              <span className={styles.balance_right}>
                {this.state.my_balance_paxg ? format_num_to_K(format_bn(this.state.my_balance_paxg, 18, 2)) : '...'}
              </span>
            </div>

            <div className={styles.balance_line}></div>

            <div className={styles.balance}>
              <span className={styles.balance_left}>
                <FormattedMessage id='Goldx_Outstanding' />
              </span>
              <span className={styles.balance_right}>
                {this.state.totalSupply_goldx ? format_num_to_K(format_bn(this.state.totalSupply_goldx, 18, 2)) : '...'}
              </span>
            </div>
            <div className={styles.balance}>
              <span className={styles.balance_left}>
                <FormattedMessage id='PAXG_Total_Supply' />
              </span>
              <span className={styles.balance_right}>
                {this.state.totalSupply_paxg ? format_num_to_K(format_bn(this.state.totalSupply_paxg, 18, 2)) : '...'}
              </span>
            </div>
            <div className={styles.balance}>
              <span className={styles.balance_left}>
                <FormattedMessage id='Total_PAXG_in_Goldx' />
              </span>
              <span className={styles.balance_right}>
                {this.state.balanceOf_paxg ? format_num_to_K(format_bn(this.state.balanceOf_paxg, 18, 2)) : '...'}
              </span>
            </div>
          </div>
        </div>

        {/* foot */}
        <div className="foot">
          <div className="foot-item">
            <div className="foot-item-title">
              <FormattedMessage id='Resource' />
            </div>
            <div className="foot-item-content">
              <a href='https://github.com/dforce-network/GOLDx' target='_blank' rel="noopener noreferrer">
                GitHub
                </a>
            </div>
            <div className="foot-item-content">
              <a
                href={'https://github.com/dforce-network/documents/tree/master/audit_report/GOLDx'}
                target='_blank'
                rel="noopener noreferrer"
              >
                Audit Report
                </a>
            </div>
          </div>

          <div className="foot-item">
            <div className="foot-item-title">
              <FormattedMessage id='Community' />
            </div>
            <div className="foot-item-content icom-a">
              <a href='https://twitter.com/dForcenet' target='_blank' rel="noopener noreferrer">
                <img alt='' src={Twitter} />
              </a>
              <a href='https://t.me/dforcenet' target='_blank' rel="noopener noreferrer">
                <img alt='' src={Telegram} />
              </a>
              <a href='https://medium.com/dforcenet' target='_blank' rel="noopener noreferrer">
                <img alt='' src={Medium} />
              </a>
              <a href='https://www.reddit.com/r/dForceNetwork' target='_blank' rel="noopener noreferrer">
                <img alt='' src={Reddit} />
              </a>
              <a href='https://discord.gg/Gbtd3MR' target='_blank' rel="noopener noreferrer">
                <img alt='' src={Discord} />
              </a>
              <a href='https://www.linkedin.com/company/dforce-network' target='_blank' rel="noopener noreferrer">
                <img alt='' src={LinkedIn} />
              </a>
              <a href='https://www.youtube.com/channel/UCM6Vgoc-BhFGG11ZndUr6Ow' target='_blank' rel="noopener noreferrer">
                <img alt='' src={Youtube} />
              </a>
              {
                this.state.cur_language === '中文' &&
                <span className='weixin-img-wrap'>
                  <img alt='' src={weixin} />
                  <img alt='' className='weixin-img' src={erweima} />
                </span>
              }
            </div>

            <div className='footer-right-fixed'>
              <div className='fixed1'>
                {
                  this.state.cur_language === '中文' ? '中文简体' : 'English'
                }
              </div>
              <span className='fixed-img'>
                <img alt='' src={arrow_u} />
              </span>
              <div className='fixed2'>
                <ul>
                  <li onClick={() => { this.setState({ cur_language: '中文' }) }}>{'中文简体'}</li>
                  <li onClick={() => { this.setState({ cur_language: 'English' }) }}>{'English'}</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="foot-item padding-left20">
            <div className="foot-item-title">
              <FormattedMessage id='Contract_US' />
            </div>
            <div className="foot-item-content">bd@dforce.network</div>
            <div className="foot-item-content">contact@dforce.network</div>
          </div>
          <div className="clear"></div>
        </div>
      </IntlProvider>
    );
  }

}
