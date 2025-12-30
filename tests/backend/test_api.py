import pytest
import sys
import os
import json

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    rv = client.get('/health')
    assert rv.status_code == 200
    assert rv.json['status'] == 'ok'

def test_list_datasets(client):
    rv = client.get('/api/datasets')
    assert rv.status_code == 200
    assert 'datasets' in rv.json
    # We expect at least karate.gml if setup ran
    datasets = [d['id'] for d in rv.json['datasets']]
    assert 'karate.gml' in datasets

def test_analyze_lpa(client):
    # Test Label Propagation on Karate
    data = {
        'graph_id': 'karate.gml',
        'algorithm': 'label_propagation'
    }
    rv = client.post('/api/analyze', json=data)
    assert rv.status_code == 200
    res = rv.json
    assert res['status'] == 'completed'
    assert 'results' in res
    assert len(res['results']) > 0
    # Check structure
    first = res['results'][0]
    assert 'node' in first
    assert 'community' in first
