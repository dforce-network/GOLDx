import React from "react";
import { FormattedMessage } from "react-intl";
import AccordionItem from "./AccordionItem";

export default function Accordion(props) {
  let [bindIndex, setBindIndex] = React.useState(props.defaultIndex);
  let arrIndex = [...bindIndex];
  const changeItem = (itemIndex) => {
    arrIndex.includes(itemIndex)
      ? (arrIndex = arrIndex.filter((n) => n !== itemIndex))
      : arrIndex.push(itemIndex);
    setBindIndex(arrIndex);
    if (typeof props.onItemClick === "function") props.onItemClick(bindIndex);
  };
  return (
    <div className={"faq"}>
      <h2>
        <FormattedMessage id="FAQ" />
      </h2>
      <ul>
        {props.children.map(({ props }) => (
          <AccordionItem
            isCollapsed={bindIndex.includes(props.index) ? true : false}
            label={props.label}
            svgName={props.svgName}
            handleClick={() => changeItem(props.index)}
            children={props.children}
            key={props.index}
          />
        ))}
      </ul>
    </div>
  );
}
