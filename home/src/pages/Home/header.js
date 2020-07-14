import React, { Component } from "react";
import { FormattedMessage } from "react-intl";
import SvgIcon from "../../components/SvgIcon/index";

export default class header extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isOpen: false,
      menuOpen: false,
      showMobileOpen: ["1", "2", "3"]
    };
  }
  showMenu(e) {
    this.setState({
      menuOpen: true,
    });
  }
  hideMenu(e) {
    this.setState({
      menuOpen: false,
    });
  }
  switch() {
    this.setState({
      isOpen: !this.state.isOpen,
    });
  }
  checked(e) {
    const language = e.target.dataset.id;
    e.stopPropagation();
    this.setState({
      isOpen: false,
    });
    this.props.setLanguage(language);
  }
  showMobileNav(index) {
    const { showMobileOpen } = this.state
    let newIndexArray = [...showMobileOpen]
    newIndexArray.includes(index) ? newIndexArray = newIndexArray.filter(n => n !== index) : newIndexArray.push(index)
    this.setState({
      showMobileOpen: newIndexArray
    })
  }
  componentDidMount() {
    document.body.addEventListener("click", (e) => {
      // if (e.target && e.target.matches('.switch_language')) {
      //   return;
      // }
      this.setState({
        isOpen: false
      })
    })
  }
  render() {
    const { isOpen, menuOpen, showMobileOpen } = this.state;
    const { cur_language } = this.props;
    return (
      <header>
        <div className="menu_header">
          <SvgIcon className={"logo"} iconClass={"logo"} alt={"dForce"} />
          <div onClick={(e) => this.showMenu(e)}><SvgIcon className={"menu_m_open"} iconClass={"meun_m_open"} /></div>
        </div>
        <nav className={"pc_nav"}>
          <div className={"active"}>
            <a className={"link"} href="https://usdx.dforce.network/">
              <FormattedMessage id="Assets" />
            </a>
            <ul>
              <li>
                <a href="https://usdx.dforce.network/">
                  <FormattedMessage id="Assets1" />
                </a>
              </li>
              <li>
                <a href="https://usdx.dforce.network/">
                  <FormattedMessage id="Assets2" />
                </a>
              </li>
            </ul>
          </div>
          <div>
            <a className={"link"} href="https://trade.dforce.network/">
              <FormattedMessage id="Trade" />
            </a>
            <ul>
              <li>
                <a href="https://trade.dforce.network/">
                  <FormattedMessage id="Trade1" />
                </a>
              </li>
              <li>
                <a href="https://trade.dforce.network/">
                  <FormattedMessage id="Trade2" />
                </a>
              </li>
            </ul>
          </div>
          <div>
            <a className={"link"} href="https://airdrop.dforce.network/">
              <FormattedMessage id="Governance" />
            </a>
            <ul>
              <li>
                <a href="https://airdrop.dforce.network/">
                  <FormattedMessage id="Governance1" />
                </a>
              </li>
              <li>
                <a href="https://airdrop.dforce.network/">
                  <FormattedMessage id="Governance2" />
                </a>
              </li>
            </ul>
          </div>
          <div className={isOpen ? "switch_language open" : "switch_language"} onClick={() => this.switch()}>
            {cur_language === "cn" ? "中文简体" : "English"}
            <SvgIcon className={"language"} iconClass={"up"} />
            <ul onClick={(e) => this.checked(e)}>
              <li data-id={"cn"}>
                <SvgIcon iconClass={"cn"} />
                中文简体
              </li>
              <li data-id={"en"}>
                <SvgIcon iconClass={"en"} />
                English
              </li>
            </ul>
          </div>
        </nav>
        <nav className={menuOpen ? 'm_nav showNav' : 'm_nav'}>
          <div className="menu_header">
            <SvgIcon className={"logo"} iconClass={"logo"} alt={"dForce"} />
            <div className={"menu_open_div"} onClick={(e) => this.hideMenu(e)}><SvgIcon className={"menu_m_open"} iconClass={"meun_m_closed"} /></div>
          </div>
          <div className={showMobileOpen.includes("1") ? "active nav_link" : "nav_link"}>
            <div className={"nav_link_title first"} onClick={() => this.showMobileNav("1")}>
              <span><FormattedMessage id="Assets" /></span>
              <SvgIcon className={"arrow"} iconClass={"arrow_up"} />
            </div>
            <ul>
              <li>
                <a href="https://usdx.dforce.network/">
                  <FormattedMessage id="Assets1" />
                </a>
              </li>
              <li>
                <a href="https://usdx.dforce.network/">
                  <FormattedMessage id="Assets2" />
                </a>
              </li>
            </ul>
          </div>
          <div className={showMobileOpen.includes("2") ? "active nav_link" : "nav_link"}>
            <div className={"nav_link_title"} onClick={() => this.showMobileNav("2")}>
              <span><FormattedMessage id="Trade" /></span>
              <SvgIcon className={"arrow"} iconClass={"arrow_up"} />
            </div>
            <ul>
              <li>
                <a href="https://trade.dforce.network/">
                  <FormattedMessage id="Trade1" />
                </a>
              </li>
              <li>
                <a href="https://trade.dforce.network/">
                  <FormattedMessage id="Trade2" />
                </a>
              </li>
            </ul>
          </div>
          <div className={showMobileOpen.includes("3") ? "active nav_link" : "nav_link"}>
            <div className={"nav_link_title"} onClick={() => this.showMobileNav("3")}>
              <span><FormattedMessage id="Governance" /></span>
              <SvgIcon className={"arrow"} iconClass={"arrow_up"} />
            </div>
            <ul>
              <li>
                <a href="https://airdrop.dforce.network/">
                  <FormattedMessage id="Governance1" />
                </a>
              </li>
              <li>
                <a href="https://airdrop.dforce.network/">
                  <FormattedMessage id="Governance2" />
                </a>
              </li>
            </ul>
          </div>
        </nav>
      </header>
    );
  }
  componentWillUnmount() {
    document.body.removeEventListener("click")
  }
}
