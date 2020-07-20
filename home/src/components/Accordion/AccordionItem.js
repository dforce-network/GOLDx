import React from "react";
import SvgIcon from "../SvgIcon";
export default function AccordionItem(props) {
  return (
    <li
      className={props.isCollapsed === false ? "" : "open"}
      onClick={() => props.handleClick()}
    >
      <div className={"faq_header"}>
        <SvgIcon className={"faq_l"} iconClass={props.svgName} />
        <span>{props.label}</span>
        <SvgIcon
          className={"faq_r"}
          iconClass={props.isCollapsed === false ? "collapse" : "unfold"}
        />
      </div>
      <div className="collapse-content" aria-expanded={props.isCollapsed}>
        {props.children}
      </div>
    </li>
  );
}
