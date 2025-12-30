import React, { useEffect, useRef } from 'react';
import CytoscapeComponent from 'react-cytoscapejs';
import cytoscape from 'cytoscape';

export default function GraphVisualizer({ elements, communityMapping }) {
    const cyRef = useRef(null);

    // Define colors for communities
    const colors = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98FB98',
        '#DDA0DD', '#F0E68C', '#87CEFA', '#FFB6C1', '#20B2AA'
    ];

    const getCommunityColor = (commId) => {
        if (!commId) return '#888';
        const index = parseInt(commId) % colors.length;
        return colors[index];
    };

    useEffect(() => {
        if (cyRef.current) {
            const cy = cyRef.current;
            cy.elements().remove();
            cy.add(elements);

            if (communityMapping && communityMapping.length > 0) {
                cy.batch(() => {
                    cy.nodes().forEach(node => {
                        const id = node.id();
                        const entry = communityMapping.find(c => String(c.node) === String(id));
                        if (entry) {
                            node.data('community', entry.community);
                            node.style('background-color', getCommunityColor(entry.community));
                        }
                    });
                });
            }

            const l = cy.layout({ name: 'cose', animate: true, padding: 30 });
            l.run();
        }
    }, [elements, communityMapping]);

    const layout = { name: 'cose', animate: true };

    const stylesheet = [
        {
            selector: 'node',
            style: {
                'background-color': '#adb5bd',
                'label': 'data(id)',
                "text-valign": "center",
                "text-halign": "center",
                "color": "#fff",
                "text-outline-width": 1,
                "text-outline-color": "#334155",
                'font-size': '10px',
                'width': 25,
                'height': 25,
                'transition-property': 'background-color, border-width, border-color',
                'transition-duration': '0.3s'
            }
        },
        {
            selector: 'node:selected',
            style: {
                'border-width': 3,
                'border-color': '#6366f1'
            }
        },
        {
            selector: 'edge',
            style: {
                'width': 1.5,
                'line-color': '#cbd5e1',
                'target-arrow-color': '#cbd5e1',
                'target-arrow-shape': 'thin-triangle',
                'curve-style': 'bezier',
                'opacity': 0.6
            }
        }
    ];

    return (
        <div style={{ flex: 1, position: 'relative', background: '#fff', height: '100%', minHeight: '600px' }}>
            <CytoscapeComponent
                elements={elements}
                style={{ width: '100%', height: '100%' }}
                stylesheet={stylesheet}
                layout={layout}
                cy={(cy) => { cyRef.current = cy; }}
            />
        </div>
    );
}
