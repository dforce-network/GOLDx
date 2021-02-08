import React, { Component, Fragment } from "react";
import { FormattedMessage } from "react-intl";
import AccordionItem from "../../components/Accordion/AccordionItem";
import Accordion from "../../components/Accordion/Accordion";

export default class FAQ extends Component {
  render() {
    const { cur_language } = this.props;
    return (
      <Accordion onItemClick={console.log} defaultIndex={[]}>
        <AccordionItem
          label={<FormattedMessage id="FAQ1" />}
          svgName={"fqa1"}
          index="1"
        >
          <p>
            <FormattedMessage id="FAQ1_text" />
          </p>
        </AccordionItem>
        <AccordionItem
          label={<FormattedMessage id="FAQ2" />}
          svgName={"fqa2"}
          index="2"
        >
          <p>
            <FormattedMessage id="FAQ2_text" />
          </p>
        </AccordionItem>
        <AccordionItem
          label={<FormattedMessage id="FAQ3" />}
          svgName={"fqa3"}
          index="3"
        >
          <p>
            <FormattedMessage id="FAQ3_1_text" />
          </p>
          <p>
            <FormattedMessage id="FAQ3_2_text" />
          </p>
        </AccordionItem>
        <AccordionItem
          label={<FormattedMessage id="FAQ4" />}
          svgName={"fqa4"}
          index="4"
        >
          <p>
            <FormattedMessage id="FAQ4_1_text" />
            <a href="mailto:support@dforce.netword">
              <FormattedMessage id="FAQ4_mail_text" />
            </a>
            <FormattedMessage id="FAQ4_2_text" />
          </p>
        </AccordionItem>
        <AccordionItem
          label={<FormattedMessage id="FAQ5" />}
          svgName={"fqa5"}
          index="5"
        >
          <p>
            <FormattedMessage id="FAQ5_text" />
          </p>
        </AccordionItem>
        <AccordionItem
          label={<FormattedMessage id="FAQ6" />}
          svgName={"fqa6"}
          index="6"
        >
          <p>
            <FormattedMessage id="FAQ6_1_text" />
            {cur_language === "cn" ? (
              <a
                href="https://github.com/dforce-network/documents/blob/master/audit_report/GOLDx/CN/SmartContractSecurityAudit-GOLDx.pdf"
                target="_blank"
                rel="noopener noreferrer"
              >
                <FormattedMessage id="FAQ6_2_text" />
              </a>
            ) : (
                <a
                  href="https://github.com/dforce-network/documents/blob/master/audit_report/GOLDx/EN/SmartContractSecurityAudit-GOLDx.pdf"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <FormattedMessage id="FAQ6_2_text" />
                </a>
              )}
            <FormattedMessage id="FAQ6_3_text" />
          </p>
        </AccordionItem>
        <AccordionItem
          label={<FormattedMessage id="FAQ7" />}
          svgName={"fqa7"}
          index="7"
        >
          {cur_language === "cn" ? (
            <Fragment>
              <p>
                <FormattedMessage id="FAQ7_1_text" />
              </p>
              <p>
                <FormattedMessage id="FAQ7_2_text" />
                <a
                  href="https://www.paxos.com/paxgold/"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <FormattedMessage id="FAQ7_3_text" />
                </a>
              </p>
            </Fragment>
          ) : (
              <Fragment>
                <p>
                  <FormattedMessage id="FAQ7_1_text" />
                </p>
                <p>
                  <FormattedMessage id="FAQ7_2_text" />
                  <a
                    href="https://www.paxos.com/paxgold/"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <FormattedMessage id="FAQ7_3_text" />
                  </a>
                  <FormattedMessage id="FAQ7_4_text" />
                </p>
              </Fragment>
            )}
        </AccordionItem>
      </Accordion>
    );
  }
}
