import { useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";

function TransactionGraph() {
  const nodes = useMemo(
    () => [
      {
        id: "wallet-a",
        position: { x: 50, y: 180 },
        data: {
          label: (
            <div>
              <strong>WALLET A</strong>
              <br />
              <small>0x8A...42F</small>
            </div>
          ),
        },
        style: {
          background: "#101923",
          color: "#ffffff",
          border: "2px solid #526477",
          borderRadius: "10px",
          padding: "12px",
          width: 150,
          textAlign: "center",
        },
      },

      {
        id: "target",
        position: { x: 280, y: 180 },
        data: {
          label: (
            <div>
              <strong>TARGET WALLET</strong>
              <br />
              <small>INVESTIGATION TARGET</small>
            </div>
          ),
        },
        style: {
          background: "#24100f",
          color: "#ffffff",
          border: "2px solid #ff3b30",
          borderRadius: "10px",
          padding: "12px",
          width: 170,
          textAlign: "center",
        },
      },

      {
        id: "wallet-b",
        position: { x: 540, y: 80 },
        data: {
          label: (
            <div>
              <strong>WALLET B</strong>
              <br />
              <small>0x31...9AC</small>
            </div>
          ),
        },
        style: {
          background: "#101923",
          color: "#ffffff",
          border: "2px solid #526477",
          borderRadius: "10px",
          padding: "12px",
          width: 150,
          textAlign: "center",
        },
      },

      {
        id: "suspicious",
        position: { x: 540, y: 280 },
        data: {
          label: (
            <div>
              <strong>SUSPICIOUS</strong>
              <br />
              <small>0x91...77D</small>
            </div>
          ),
        },
        style: {
          background: "#29100e",
          color: "#ffffff",
          border: "2px solid #ff5147",
          borderRadius: "10px",
          padding: "12px",
          width: 150,
          textAlign: "center",
        },
      },

      {
        id: "exchange",
        position: { x: 790, y: 280 },
        data: {
          label: (
            <div>
              <strong>VASP / EXCHANGE</strong>
              <br />
              <small>UNKNOWN</small>
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
      },
    ],
    []
  );

  const edges = useMemo(
    () => [
      {
        id: "edge-1",
        source: "wallet-a",
        target: "target",
        animated: true,
        style: {
          stroke: "#8c98a6",
          strokeWidth: 2,
        },
      },

      {
        id: "edge-2",
        source: "target",
        target: "wallet-b",
        animated: true,
        style: {
          stroke: "#8c98a6",
          strokeWidth: 2,
        },
      },

      {
        id: "edge-3",
        source: "target",
        target: "suspicious",
        animated: true,
        style: {
          stroke: "#ff5147",
          strokeWidth: 3,
        },
      },

      {
        id: "edge-4",
        source: "suspicious",
        target: "exchange",
        animated: true,
        style: {
          stroke: "#63c77a",
          strokeWidth: 2,
        },
      },
    ],
    []
  );

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
        fitViewOptions={{
          padding: 0.25,
        }}
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