import React from "react";
import { FormattedMessage } from "react-intl";
import SvgIcon from "../../components/SvgIcon/index";
export default function Ecosystem() {
  return (
    <div className="ecosystem">
      <div className={"eco_warp"}>
        <h2>
          <FormattedMessage id="SWAP" />
        </h2>
        <p>
          <FormattedMessage id="GOLDxEcosystemTitle1" />
          <br />
          <FormattedMessage id="GOLDxEcosystemTitle2" />
        </p>
        <ul className={""}>
          <li>
            <a
              target="_blank"
              rel="noopener noreferrer"
              href="https://www.slowmist.com/"
            >
              <SvgIcon iconClass={"ecosystem1"} />
              <span>SlowMist</span>
            </a>
          </li>
          <li>
            <a
              target="_blank"
              rel="noopener noreferrer"
              href="https://www.paxos.com/paxgold/"
            >
              <SvgIcon iconClass={"ecosystem2"} />
              <span>Paxos Gold</span>
            </a>
          </li>
          <li>
            <a
              target="_blank"
              rel="noopener noreferrer"
              href="https://dforce.network/"
            >
              <SvgIcon iconClass={"ecosystem3"} />
              <span>dForce Hybrid Lending</span>
            </a>
          </li>
          <li>
            <a
              target="_blank"
              rel="noopener noreferrer"
              href="https://trade.dforce.network/"
            >
              <SvgIcon iconClass={"ecosystem3"} />
              <span>dForce Trade</span>
            </a>
          </li>
          <li>
            <a
              target="_blank"
              rel="noopener noreferrer"
              href="https://token.im/"
            >
              <SvgIcon iconClass={"imToken"} />
              <span>imToken Wallet</span>
            </a>
          </li>
          <li>
            <a
              target="_blank"
              rel="noopener noreferrer"
              href="https://bitpie.com/"
            >
              <SvgIcon iconClass={"bitpie"} />
              <span>Bitpie Wallet</span>
            </a>
          </li>
          <li>
            <a
              target="_blank"
              rel="noopener noreferrer"
              href="https://mykey.org/"
            >
              <SvgIcon iconClass={"mykey"} />
              <span>MYKEY Wallet</span>
            </a>
          </li>
          <li>
            <a
              target="_blank"
              rel="noopener noreferrer"
              href="https://www.tokenpocket.pro/"
            >
              <SvgIcon iconClass={"TOKENPOCKET"} />
              <span>TOKENPOCKET Wallet</span>
            </a>
          </li>
          <li>
            <a
              target="_blank"
              rel="noopener noreferrer"
              href="https://www.huobiwallet.com/"
            >
              <SvgIcon iconClass={"huobi"} />
              <span>Huobi Wallet</span>
            </a>
          </li>
          <li>
            <a
              target="_blank"
              rel="noopener noreferrer"
              href="https://cobo.com/"
            >
              <SvgIcon iconClass={"cobo"} />
              <span>cobo Wallet</span>
            </a>
          </li>
          <li>
            <a
              target="_blank"
              rel="noopener noreferrer"
              href="https://www.mathwallet.org/en-us/"
            >
              <SvgIcon iconClass={"MathWallet"} />
              <span>Math Wallet</span>
            </a>
          </li>
          <li>
            <a
              target="_blank"
              rel="noopener noreferrer"
              href="https://dappbirds.com/index"
            >
              <SvgIcon iconClass={"Dappbirds"} />
              <span>Dappbirds Wallet</span>
            </a>
          </li>
        </ul>
      </div>
    </div>
  );
}
