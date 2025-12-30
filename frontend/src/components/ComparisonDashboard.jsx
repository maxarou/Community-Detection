import React from 'react';

export default function ComparisonDashboard({ results }) {
    if (!results || results.length === 0) return null;

    return (
        <div className="comparison-dashboard" style={{
            background: 'white',
            padding: '20px',
            borderRadius: '12px',
            boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
            marginTop: '20px'
        }}>
            <h3 style={{ marginTop: 0 }}>📈 Benchmark Comparative</h3>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                    <tr style={{ borderBottom: '2px solid #f1f5f9', textAlign: 'left' }}>
                        <th style={{ padding: '10px' }}>Algorithme</th>
                        <th style={{ padding: '10px' }}>Commu.</th>
                        <th style={{ padding: '10px' }}>Modularity (Q)</th>
                        <th style={{ padding: '10px' }}>Score</th>
                    </tr>
                </thead>
                <tbody>
                    {results.map((res, i) => (
                        <tr key={i} style={{ borderBottom: '1px solid #f1f5f9' }}>
                            <td style={{ padding: '10px', fontWeight: 600 }}>{res.algorithm}</td>
                            <td style={{ padding: '10px' }}>{res.numCommunities}</td>
                            <td style={{ padding: '10px' }}>{res.modularity}</td>
                            <td style={{ padding: '10px' }}>
                                <div style={{
                                    height: '8px',
                                    width: `${Math.max(2, res.modularity * 100)}%`,
                                    background: res.modularity > 0 ? '#6366f1' : '#e2e8f0',
                                    borderRadius: '4px',
                                    transition: 'width 0.4s ease'
                                }}></div>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
