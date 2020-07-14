import React, { Component } from "react";
// add i18n.
import { IntlProvider } from "react-intl";
import en_US from "../../language/en";
import zh_CN from "../../language/cn";
import Header from "./header";
import Banner from "./banner";
import Transaction from "./transaction";
import Features from "./features";
import Ecosystem from "./ecosystem";
import FAQ from "./FAQ";
import Footer from "./footer";
export default class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      cur_language: navigator.language === "zh-CN" ? "cn" : "en",
    };
  }
  setLanguage(language) {
    this.setState(() => ({ cur_language: language }));
  }
  render() {
    let { cur_language } = this.state;
    return (
      <IntlProvider
        locale={"en"}
        messages={this.state.cur_language === "cn" ? zh_CN : en_US}
      >
        <div className={"container"}>
          <Header
            cur_language={cur_language}
            setLanguage={(language) => this.setLanguage(language)}
          />
          <Banner cur_language={cur_language} />
          <Transaction />
          <Features />
          <Ecosystem />
          <FAQ cur_language={cur_language} />
          <Footer cur_language={cur_language} />
        </div>
      </IntlProvider>
    );
  }
}
