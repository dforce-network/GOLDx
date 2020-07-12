import React from "react";
import { FormattedMessage } from "react-intl";
import SvgIcon from "../../components/SvgIcon/index";
export default function Features() {
  return (
    <div className={"features"}>
      <div className={"header"}>
        <h2>
          <FormattedMessage id="Features" />
        </h2>
        <p>
          <FormattedMessage id="FeaturesTitle1" />
          <br />
          <FormattedMessage id="FeaturesTitle2" />
        </p>
      </div>
      <ul>
        <li>
          <SvgIcon
            iconClass={"features1"}
            alt={<FormattedMessage id="Customization" />}
          />
          <div className={"features_right"}>
            <h2>
              <FormattedMessage id="Customization" />
            </h2>
            <p>
              <FormattedMessage id="CustomizationContent" />
            </p>
          </div>
        </li>
        <li>
          <SvgIcon
            iconClass={"features2"}
            alt={<FormattedMessage id="PricePeg" />}
          />
          <div className={"features_right"}>
            <h2>
              <FormattedMessage id="PricePeg" />
            </h2>
            <p>
              <FormattedMessage id="PricePegContent" />
            </p>
          </div>
        </li>
        <li>
          <SvgIcon
            iconClass={"features3"}
            alt={<FormattedMessage id="Redeemability" />}
          />
          <div className={"features_right"}>
            <h2>
              <FormattedMessage id="Redeemability" />
            </h2>
            <p>
              <FormattedMessage id="RedeemabilityContent" />
            </p>
          </div>
        </li>
        <li>
          <SvgIcon
            iconClass={"features4"}
            alt={<FormattedMessage id="DeFiCompatibility" />}
          />
          <div className={"features_right"}>
            <h2>
              <FormattedMessage id="DeFiCompatibility" />
            </h2>
            <p>
              <FormattedMessage id="DeFiCompatibilityContent" />
            </p>
          </div>
        </li>
        <li>
          <SvgIcon
            iconClass={"features5"}
            alt={<FormattedMessage id="Transparency" />}
          />
          <div className={"features_right"}>
            <h2>
              <FormattedMessage id="Transparency" />
            </h2>
            <p>
              <FormattedMessage id="TransparencyContent" />
            </p>
          </div>
        </li>
        <li>
          <SvgIcon
            iconClass={"features6"}
            alt={<FormattedMessage id="EasyAccessibility" />}
          />
          <div className={"features_right"}>
            <h2>
              <FormattedMessage id="EasyAccessibility" />
            </h2>
            <p>
              <FormattedMessage id="EasyAccessibilityContent" />
            </p>
          </div>
        </li>
        <li>
          <SvgIcon
            iconClass={"features7"}
            alt={<FormattedMessage id="InterestBearing" />}
          />
          <div className={"features_right"}>
            <h2>
              <FormattedMessage id="InterestBearing" />
            </h2>
            <p>
              <FormattedMessage id="InterestBearingContent" />
            </p>
          </div>
        </li>
        <li>
          <SvgIcon
            iconClass={"features8"}
            alt={<FormattedMessage id="Upgradability" />}
          />
          <div className={"features_right"}>
            <h2>
              <FormattedMessage id="Upgradability" />
            </h2>
            <p>
              <FormattedMessage id="UpgradabilityContent" />
            </p>
          </div>
        </li>
      </ul>
    </div>
  );
}
