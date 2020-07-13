import React, { Component } from "react";
import { FormattedMessage } from "react-intl";
import SvgIcon from "../../components/SvgIcon/index";

export default class header extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isOpen: false,
    };
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
  componentDidMount() {
    document.body.addEventListener("click", (e) => {
      if (e.target && e.target.matches('.switch_language')) {
        return;
      }
      this.setState({
        isOpen: false
      })
    })
  }
  render() {
    const { isOpen } = this.state;
    const { cur_language } = this.props;
    return (
      <header>
        <SvgIcon className={"logo"} iconClass={"logo"} alt={"dForce"} />
        <nav>
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
      </header>
    );
  }
  componentWillUnmount() {
    document.body.removeEventListener("click")
  }
}
