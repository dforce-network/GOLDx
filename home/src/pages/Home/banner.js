import React from "react";
import { FormattedMessage } from "react-intl";
import SvgIcon from "../../components/SvgIcon/index";
import banner_cn from "../../static/img/banner-cn.png";
import banner_en from "../../static/img/banner-en.png";
function Banner(props) {
  return (
    <div className={"banner"}>
      <div className={"svgbg"}></div>
      <div className={"banner_warp"}>
        {props.cur_language === "cn" ? (
          <p className={"goldx"}>
            <FormattedMessage id="bannerTitle1" />
            &nbsp;
            <span>
              <FormattedMessage id="bannerTitle2" />
            </span>
          </p>
        ) : (
            <p className={"goldx"}>
              <span>
                <FormattedMessage id="bannerTitle1" />
              </span>
              <FormattedMessage id="bannerTitle2" />
              <span>
                <FormattedMessage id="bannerTitle3" />
              </span>
            </p>
          )}
        <p>
          <FormattedMessage id="bannerSection1" />
        </p>
        <p>
          <FormattedMessage id="bannerSection2" />
        </p>
        <p>
          <FormattedMessage id="bannerSection3" />
        </p>
      </div>
      {/* <div className={props.cur_language === "cn" ? "m_warp" : "m_warp_en"}>
        {props.cur_language === "cn" ? (
          // <SvgIcon iconClass={"banner_cn"} />
          <img src={banner_cn} className={"banner_cn"} />
        ) : (
          // <SvgIcon iconClass={"banner_en"} />
          <img src={banner_en} className={"banner_en"} />
        )}
      </div> */}
      <div
        className={
          props.cur_language === "cn" ? "btn_box" : "btn_box btn_box_en"
        }
      >
        {props.cur_language === "cn" ? (
          <a
            href="https://github.com/dforce-network/documents/blob/master/white_papers/cn/Goldx_Whitepaper.pdf"
            target="_blank"
            rel="noopener noreferrer"
            className={"btn active"}
          >
            <FormattedMessage id="WhitePaper" />
          </a>
        ) : (
            <a
              href="https://github.com/dforce-network/documents/blob/master/white_papers/en/GOLDx_Whitepaper.pdf"
              className={"btn active"}
            >
              <FormattedMessage id="WhitePaper" />
            </a>
          )}
        <a href="/dapp" className={"btn"}>
          <FormattedMessage id="Mint" />
        </a>
        <a
          href="https://trade.dforce.network/"
          className={"m_btn active"}
          target="_blank"
          rel="noopener noreferrer"
        >
          <FormattedMessage id="swap" />
        </a>
      </div>
    </div>
  );
}
export default Banner;
