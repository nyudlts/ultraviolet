import React from "react";

export const WfsAttributeTable = (
  {
    attributes = []
  }
) => {
  if (!attributes) {
    return <>No data to display.</>
  }

  const attributeRows = attributes.map(attribute => <tr key={attribute.name}>
    <td>{attribute.name}</td>
    <td>{attribute.localType}</td>
  </tr>)

  return <table className="ui unstackable very compact table striped selectable">
    <thead>
    <tr>
      <th>Name</th>
      <th>Type</th>
    </tr>
    </thead>
    <tbody>
    {attributeRows}
    </tbody>
  </table>
}
