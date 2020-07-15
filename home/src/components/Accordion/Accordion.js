import React from "react";
import { FormattedMessage } from "react-intl";
import AccordionItem from "./AccordionItem";

export default function Accordion(props) {
  const [bindIndex, setBindIndex] = React.useState(props.defaultIndex);

  const changeItem = (itemIndex) => {
    if (typeof props.onItemClick === "function") props.onItemClick(itemIndex);
    if (itemIndex !== bindIndex) setBindIndex(itemIndex);
  };
  //   const items = props.children.filter(
  //     (item) => item.type.name === "AccordionItem"
  //   );
  //   console.log(items);
  return (
    <div className={"faq"}>
      <h2><FormattedMessage id="FAQ" /></h2>
      <ul>
        {props.children.map(({ props }) => (
          <AccordionItem
            isCollapsed={bindIndex !== props.index}
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
