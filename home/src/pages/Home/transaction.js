import React from "react";
import { FormattedMessage } from "react-intl";
// import SvgIcon from "../../components/SvgIcon/index";
export default function Transaction() {
  return (
    <div className={"transaction"}>
      <div className={"trans_warp"}>
        <div className={"top"}></div>
        <a href="https://trade.dforce.network/" className={"btn"}>
          <FormattedMessage id="swap" />
        </a>
      </div>
    </div>
  );
}
