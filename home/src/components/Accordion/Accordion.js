import React from 'react'
import AccordionItem from './AccordionItem'

export default function Accordion(props) {
    const [bindIndex, setBindIndex] = React.useState(props.defaultIndex);

    const changeItem = itemIndex => {
        if (typeof props.onItemClick === 'function') props.onItemClick(itemIndex);
        if (itemIndex !== bindIndex) setBindIndex(itemIndex);
    };
    const items = props.children.filter(item => item.type.name === 'AccordionItem');

    return (
        <div className={"faq"}>
            <h2>常见问题</h2>
            <ul>
                {items.map(({ props }) => (
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