import React from 'react';

export default function MetricsPanel({ communities, computationTime }) {
    if (!communities || communities.length === 0) return null;

    // Calculate basic metrics
    const communityCounts = {};
    communities.forEach(c => {
        const label = c.community;
        communityCounts[label] = (communityCounts[label] || 0) + 1;
    });

    const numCommunities = Object.keys(communityCounts).length;
    const sortedSizes = Object.values(communityCounts).sort((a, b) => b - a);

    return (
        <div className="metrics-panel" style={{
            background: 'white',
            padding: '15px',
            borderRadius: '8px',
            border: '1px solid #e0e0e0',
            boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
            marginTop: '20px',
            minWidth: '250px'
        }}>
            <h3 style={{ marginTop: 0, color: '#2c3e50' }}>📊 Résultats</h3>

            <div className="metric-row">
                <strong>Communautés détectées:</strong> {numCommunities}
            </div>

            {computationTime && (
                <div className="metric-row">
                    <strong>Temps de calcul:</strong> {computationTime} ms
                </div>
            )}

            <h4 style={{ marginBottom: '5px' }}>Distribution des tailles</h4>
            <div className="size-bars" style={{ display: 'flex', gap: '5px', alignItems: 'flex-end', height: '60px' }}>
                {sortedSizes.map((size, idx) => (
                    <div key={idx} style={{
                        background: '#3498db',
                        width: '20px',
                        height: `${(size / sortedSizes[0]) * 100}%`,
                        borderRadius: '2px 2px 0 0',
                        textAlign: 'center',
                        fontSize: '0.8em',
                        color: 'white'
                    }} title={`Community ${idx}: ${size} nodes`}>
                    </div>
                ))}
            </div>
            <div style={{ fontSize: '0.8em', color: '#7f8c8d', marginTop: '5px' }}>
                Plus grande: {sortedSizes[0]} nœuds
            </div>
        </div>
    );
}
