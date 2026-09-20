import { useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";

// This component now takes real data from the backend as a prop,
// instead of showing the same hardcoded fake wallets every time.

function TransactionGraph({ data }) {
  const nodes = useMemo(() => {
    if (!data) return [];

    const centerX = 400;
    const centerY = 250;

    const nodeList = [
      {
        id: "target",
        position: { x: centerX, y: centerY },
        data: {
          label: (
            <div>
              <strong>TARGET WALLET</strong>
              <br />
              <small>{data.wallet_address}</small>
            </div>
          ),
        },
        style: {
          background: data.has_overlap ? "#24100f" : "#101923",
          color: "#ffffff",
          border: data.has_overlap
            ? "2px solid #ff3b30"
            : "2px solid #63c77a",
          borderRadius: "10px",
          padding: "12px",
          width: 200,
          textAlign: "center",
        },
      },
    ];

    const activeCases = data.overlapping_active_cases || [];
    activeCases.forEach((c, index) => {
      nodeList.push({
        id: `active-case-${c.id ?? index}`,
        position: {
          x: centerX + (index - (activeCases.length - 1) / 2) * 220,
          y: centerY - 200,
        },
        data: {
          label: (
            <div>
              <strong>ACTIVE CASE</strong>
              <br />
              <small>#{c.id ?? "unknown"}</small>
            </div>
          ),
        },
        style: {
          background: "#29100e",
          color: "#ffffff",
          border: "2px solid #ff5147",
          borderRadius: "10px",
          padding: "12px",
          width: 160,
          textAlign: "center",
        },
      });
    });

    const pastCases = data.overlapping_past_cases || [];
    pastCases.forEach((c, index) => {
      nodeList.push({
        id: `past-case-${c.id ?? index}`,
        position: {
          x: centerX + (index - (pastCases.length - 1) / 2) * 220,
          y: centerY + 200,
        },
        data: {
          label: (
            <div>
              <strong>PAST CASE</strong>
              <br />
              <small>#{c.id ?? "unknown"}</small>
            </div>
          ),
        },
        style: {
          background: "#101923",
          color: "#ffffff",
          border: "2px solid #8c98a6",
          borderRadius: "10px",
          padding: "12px",
          width: 160,
          textAlign: "center",
        },
      });
    });

    if (data.is_known_entity && data.known_entity_details) {
      nodeList.push({
        id: "known-entity",
        position: { x: centerX + 320, y: centerY },
        data: {
          label: (
            <div>
              <strong>KNOWN ENTITY</strong>
              <br />
              <small>
                {data.known_entity_details.name || "Flagged Entity"}
              </small>
            </div>
          ),
        },
        style: {
          background: "#111923",
          color: "#ffffff",
          border: "2px solid #63c77a",
          borderRadius: "10px",
          padding: "12px",
          width: 170,
          textAlign: "center",
        },
      });
    }

    return nodeList;
  }, [data]);

  const edges = useMemo(() => {
    if (!data) return [];

    const edgeList = [];

    const activeCases = data.overlapping_active_cases || [];
    activeCases.forEach((c, index) => {
      edgeList.push({
        id: `edge-active-${c.id ?? index}`,
        source: "target",
        target: `active-case-${c.id ?? index}`,
        animated: true,
        style: { stroke: "#ff5147", strokeWidth: 2 },
      });
    });

    const pastCases = data.overlapping_past_cases || [];
    pastCases.forEach((c, index) => {
      edgeList.push({
        id: `edge-past-${c.id ?? index}`,
        source: "target",
        target: `past-case-${c.id ?? index}`,
        animated: true,
        style: { stroke: "#8c98a6", strokeWidth: 2 },
      });
    });

    if (data.is_known_entity && data.known_entity_details) {
      edgeList.push({
        id: "edge-known-entity",
        source: "target",
        target: "known-entity",
        animated: true,
        style: { stroke: "#63c77a", strokeWidth: 2 },
      });
    }

    return edgeList;
  }, [data]);

  if (!data || (!data.has_overlap && !data.is_known_entity)) {
    return (
      <div
        style={{
          width: "100%",
          height: "100%",
          background: "#070b10",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#8c98a6",
        }}
      >
        No connections found for this wallet — it does not overlap with any known cases.
      </div>
    );
  }

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "#070b10",
      }}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        fitViewOptions={{ padding: 0.25 }}
        nodesDraggable={true}
        nodesConnectable={false}
        elementsSelectable={true}
      >
        <Background gap={20} size={1} />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
}

export default TransactionGraph;