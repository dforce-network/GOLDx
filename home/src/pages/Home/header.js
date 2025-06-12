import React, { Component } from "react";
import { FormattedMessage } from "react-intl";
import SvgIcon from "../../components/SvgIcon/index";

export default class header extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isOpen: false,
      menuOpen: false,
      showMobileOpen: ["1", "2", "3"],
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
    const { showMobileOpen } = this.state;
    let newIndexArray = [...showMobileOpen];
    newIndexArray.includes(index)
      ? (newIndexArray = newIndexArray.filter((n) => n !== index))
      : newIndexArray.push(index);
    this.setState({
      showMobileOpen: newIndexArray,
    });
  }
  componentDidMount() {
    document.body.addEventListener("click", (e) => {
      if (e.target && e.target.matches(".switch_language")) {
        return;
      }
      this.setState({
        isOpen: false,
      });
    });
  }
  render() {
    const { isOpen, menuOpen, showMobileOpen } = this.state;
    const { cur_language } = this.props;
    return (
      <header>
        <div className="menu_header">
          <a href="https://dforce.network/"
            rel="noopener noreferrer"><SvgIcon className={"logo"} iconClass={"logo"} alt={"dForce"} /></a>
          {/* <div onClick={(e) => this.showMenu(e)}>
            <SvgIcon className={"menu_m_open"} iconClass={"meun_m_open"} />
          </div> */}
        </div>
        <nav className={"pc_nav"}>
          <div
            className={isOpen ? "switch_language open" : "switch_language"}
            onClick={() => this.switch()}
          >
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
    document.body.removeEventListener("click");
  }
}
