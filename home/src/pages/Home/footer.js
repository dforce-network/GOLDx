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
                <a
                  href="https://twitter.com/dForcenet"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <SvgIcon iconClass={"icon1"} />
                </a>
              </li>
              <li>
                <a
                  href="https://t.me/dforcenet"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <SvgIcon iconClass={"icon2"} />
                </a>
              </li>
              <li>
                <a
                  href="https://medium.com/dforcenet"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <SvgIcon iconClass={"icon3"} />
                </a>
              </li>
              <li>
                <a
                  href="https://www.reddit.com/r/dForceNetwork"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <SvgIcon iconClass={"icon4"} />
                </a>
              </li>
              <li>
                <a
                  href="https://discord.gg/Gbtd3MR"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <SvgIcon iconClass={"icon5"} />
                </a>
              </li>
              <li>
                <a
                  href="https://www.linkedin.com/company/dforce-network"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <SvgIcon iconClass={"icon6"} />
                </a>
              </li>
              <li>
                <a
                  href="https://www.youtube.com/channel/UCM6Vgoc-BhFGG11ZndUr6Ow"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <SvgIcon iconClass={"icon7"} />
                </a>
              </li>
              {props.cur_language === "cn" && (
                <li className={"wxCode"}>
                  <SvgIcon iconClass={"icon8"} />
                  <SvgIcon className={"code"} iconClass={"code1"} />
                </li>
              )}
            </ul>
          </div>
          <div className={"info_ct"}>
            <b>
              <FormattedMessage id="products" />
            </b>
            <a
              href="https://usdx.dforce.network/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FormattedMessage id="Assets1" />
            </a>
            <a
              href="https://trade.dforce.network/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FormattedMessage id="Trade1" />
            </a>
            <a href="/">
              <FormattedMessage id="GOLDx" />
            </a>
          </div>
          <div className={"info_ct info_r"}>
            <b>
              <FormattedMessage id="contactUs" />
            </b>
            <a href="mailto:bd@dforce.network">bd@dforce.network</a>
            <a href="mailto:tech@dforce.network">contact@dforce.network</a>
          </div>
        </div>
        <div className={"copyright"}>
          <div className={"link"}>
            {/* <a className={"active"} href="https://github.com/dforce-network">
              <FormattedMessage id="developer" />
            </a> */}
            <a
              href="https://github.com/dforce-network/GOLDx"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FormattedMessage id="GitHub" />
            </a>
            <a
              href="https://github.com/dforce-network/documents"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FormattedMessage id="Documentations" />
            </a>
            <a
              href="https://github.com/dforce-network/documents/tree/master/audit_report/GOLDx"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FormattedMessage id="AuditReports" />
            </a>
          </div>
        </div>
        <div className={"m_top_info"}>
          <div className={"info_l"}>
            <SvgIcon className={"goldx_logo"} iconClass={"goldx_logo"} />
          </div>
          <div className={"info_ct"}>
            <b>
              <FormattedMessage id="products" />
            </b>
            <a
              href="https://usdx.dforce.network/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FormattedMessage id="Assets1" />
            </a>
            <a
              href="https://trade.dforce.network/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FormattedMessage id="Trade1" />
            </a>
            <a href="/">
              <FormattedMessage id="GOLDx" />
            </a>
          </div>
          <div className={"info_ct"}>
            <b>
              <FormattedMessage id="developer" />
            </b>
            <a
              href="https://github.com/dforce-network"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FormattedMessage id="GitHub" />
            </a>
            <a
              href="https://github.com/dforce-network/documents"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FormattedMessage id="Documentations" />
            </a>
            <a
              href="https://github.com/dforce-network/documents/tree/master/audit_report"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FormattedMessage id="AuditReports" />
            </a>
          </div>
          <div className={"info_ct info_r"}>
            <b>
              <FormattedMessage id="contactUs" />
            </b>
            <div className={"info_r_link"}>
              <a href="mailto:support@dforce.network">support@dforce.network</a>
              <a href="mailto:bd@dforce.network">bd@dforce.network</a>
              <a href="mailto:tech@dforce.network">tech@dforce.network</a>
            </div>
          </div>

          <div className={"info_l"}>
            <p>
              <FormattedMessage id="foot_r" />
            </p>
            <ul className={"icon"}>
              <li>
                <a
                  href="https://twitter.com/dForcenet"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <SvgIcon iconClass={"icon1"} />
                </a>
              </li>
              <li>
                <a
                  href="https://t.me/dforcenet"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <SvgIcon iconClass={"icon2"} />
                </a>
              </li>
              <li>
                <a
                  href="https://medium.com/dforcenet"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <SvgIcon iconClass={"icon3"} />
                </a>
              </li>
              <li>
                <a
                  href="https://www.reddit.com/r/dForceNetwork"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <SvgIcon iconClass={"icon4"} />
                </a>
              </li>
              <li>
                <a
                  href="https://discord.gg/Gbtd3MR"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <SvgIcon iconClass={"icon5"} />
                </a>
              </li>
              <li>
                <a
                  href="https://www.linkedin.com/company/dforce-network"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <SvgIcon iconClass={"icon6"} />
                </a>
              </li>
              <li>
                <a
                  href="https://www.youtube.com/channel/UCM6Vgoc-BhFGG11ZndUr6Ow"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <SvgIcon iconClass={"icon7"} />
                </a>
              </li>
              {props.cur_language === "cn" && (
                <li className={"wxCode"}>
                  <SvgIcon iconClass={"icon8"} />
                  <SvgIcon className={"code"} iconClass={"code1"} />
                </li>
              )}
            </ul>
          </div>
        </div>
      </div>
    </footer>
  );
}
