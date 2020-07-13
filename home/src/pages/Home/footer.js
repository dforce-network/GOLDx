import React from "react";
import { FormattedMessage } from "react-intl";
import SvgIcon from "../../components/SvgIcon/index";
export default function Footer(props) {
  return (
    <footer>
      <div className={"footer_warp"}>
        <div className={"top_info"}>
          <div className={"info_l"}>
            <SvgIcon className={"goldx_logo"} iconClass={"goldx_logo"} />
            <p>
              <FormattedMessage id="foot_r" />
            </p>
            <ul className={"icon"}>
              <li>
                <a href="https://twitter.com/dForcenet">
                  <SvgIcon iconClass={"icon1"} />
                </a>
              </li>
              <li>
                <a href="https://t.me/dforcenet">
                  <SvgIcon iconClass={"icon2"} />
                </a>
              </li>
              <li>
                <a href="https://medium.com/dforcenet">
                  <SvgIcon iconClass={"icon3"} />
                </a>
              </li>
              <li>
                <a href="https://www.reddit.com/r/dForceNetwork">
                  <SvgIcon iconClass={"icon4"} />
                </a>
              </li>
              <li>
                <a href="https://discord.gg/Gbtd3MR">
                  <SvgIcon iconClass={"icon5"} />
                </a>
              </li>
              <li>
                <a href="https://www.linkedin.com/company/dforce-network">
                  <SvgIcon iconClass={"icon6"} />
                </a>
              </li>
              <li>
                <a href="https://www.youtube.com/channel/UCM6Vgoc-BhFGG11ZndUr6Ow">
                  <SvgIcon iconClass={"icon7"} />
                </a>
              </li>
              {
                props.cur_language === 'cn' && <li className={"wxCode"}>
                  <SvgIcon iconClass={"icon8"} />
                  <SvgIcon className={"code"} iconClass={"wx_code"} />
                </li>
              }

            </ul>
          </div>
          <div className={"info_ct"}>
            <b>
              <FormattedMessage id="products" />
            </b>
            <a href="https://usdx.dforce.network/">
              <FormattedMessage id="Assets1" />
            </a>
            <a href="https://trade.dforce.network/">
              <FormattedMessage id="Trade1" />
            </a>
          </div>
          <div className={"info_ct info_r"}>
            <b>
              <FormattedMessage id="contactUs" />
            </b>
            <a href="mailto:support@dforce.netword">support@dforce.netword</a>
            <a href="mailto:bd@dforce.netword">bd@dforce.netword</a>
            <a href="mailto:tech@dforce.netword">tech@dforce.netword</a>
          </div>
        </div>
        <div className={"copyright"}>
          <div className={"link"}>
            <a className={"active"} href="https://github.com/dforce-network">
              <FormattedMessage id="developer" />
            </a>
            <a href="https://github.com/dforce-network">
              <FormattedMessage id="GitHub" />
            </a>
            <a href="https://github.com/dforce-network/documents">
              <FormattedMessage id="Documentations" />
            </a>
            <a href="https://github.com/dforce-network/documents/tree/master/audit_report">
              <FormattedMessage id="AuditReports" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
