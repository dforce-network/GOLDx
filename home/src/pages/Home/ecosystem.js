import React from 'react'
import { FormattedMessage } from 'react-intl';
import SvgIcon from "../../components/SvgIcon/index";
export default function Ecosystem() {
    return (
        <div className="ecosystem">
            <div className={"eco_warp"}>
                <h2><FormattedMessage id='SWAP' /></h2>
                <p><FormattedMessage id='GOLDxEcosystemTitle1' /><br /><FormattedMessage id='GOLDxEcosystemTitle2' /></p>
                <ul className={""}>
                    <li>
                        <a href="https://www.slowmist.com/">
                            <SvgIcon iconClass={"ecosystem1"} />
                            <span>SlowMist</span>
                        </a>

                    </li>
                    <li>
                        <a href="https://www.paxos.com/paxgold/">
                            <SvgIcon iconClass={"ecosystem2"} />
                            <span>Paxos Gold</span>
                        </a>
                    </li>
                    <li>
                        <a href="https://dforce.network/">
                            <SvgIcon iconClass={"ecosystem3"} />
                            <span>dForce Hybrid Lending</span>
                        </a>
                    </li>
                    <li>
                        <a href="https://trade.dforce.network/">
                            <SvgIcon iconClass={"ecosystem4"} />
                            <span>dForce Swap</span>
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    )
}
