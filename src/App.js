import React, { useState, useEffect } from 'react';
import {
  Card,
  Button,
  Intent,
  H3,
  H5,
  Text,
  Callout,
  Spinner,
  Icon
} from '@blueprintjs/core';
import { Power, Refresh, Play } from '@blueprintjs/icons';
import { send_magic_packet } from 'wakeonlan';
import '@blueprintjs/core/lib/css/blueprint.css';

function App() {
  // State to store PC list and loading status
  const [pcList, setPcList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [wakingPc, setWakingPc] = useState(null);
  const [message, setMessage] = useState('');

  // Load PC list from CSV file on component mount
  useEffect(() => {
    loadPcList();
  }, []);

  // Function to load PC list from CSV
  const loadPcList = async () => {
    try {
      // In Electron, we can use Node.js fs module
      const fs = require('fs');
      const csv = require('csv-parser');
      
      const results = [];
      fs.createReadStream('list.csv')
        .pipe(csv())
        .on('data', (data) => results.push(data))
        .on('end', () => {
          setPcList(results);
          setLoading(false);
        });
    } catch (error) {
      console.error('Error loading PC list:', error);
      setMessage('Error loading PC list. Please check if list.csv exists.');
      setLoading(false);
    }
  };

  // Function to wake up a single PC
  const wakePc = async (pc) => {
    setWakingPc(pc.name);
    setMessage('');
    
    try {
      // Send magic packet using wakeonlan library
      await send_magic_packet(pc.mac, {
        ip_address: '192.168.0.255',
        port: 9
      });
      
      setMessage(`Magic packet sent to ${pc.name} (${pc.mac})`);
    } catch (error) {
      setMessage(`Error waking up ${pc.name}: ${error.message}`);
    } finally {
      setWakingPc(null);
    }
  };

  // Function to wake up all PCs
  const wakeAllPcs = async () => {
    setMessage('Waking up all PCs...');
    
    for (const pc of pcList) {
      try {
        await send_magic_packet(pc.mac, {
          ip_address: '192.168.0.255',
          port: 9
        });
        console.log(`Sent magic packet to ${pc.name}`);
      } catch (error) {
        console.error(`Error waking up ${pc.name}:`, error);
      }
    }
    
    setMessage('Magic packets sent to all PCs');
  };

  // Show loading spinner while loading PC list
  if (loading) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <Spinner size={50} />
        <H5 style={{ marginTop: '10px' }}>Loading PC list...</H5>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '30px' }}>
        <H3>
          <Icon icon={Power} style={{ marginRight: '10px' }} />
          Wake-on-LAN Controller
        </H3>
        <Text>Manage and wake up your network computers</Text>
      </div>

      {/* Message display */}
      {message && (
        <Callout 
          intent={message.includes('Error') ? Intent.DANGER : Intent.SUCCESS}
          style={{ marginBottom: '20px' }}
        >
          {message}
        </Callout>
      )}

      {/* Wake All button */}
      <Card style={{ marginBottom: '20px' }}>
        <Button
          icon={Play}
          intent={Intent.PRIMARY}
          text="Wake All PCs"
          onClick={wakeAllPcs}
          large
          fill
        />
      </Card>

      {/* PC List */}
      <div style={{ display: 'grid', gap: '10px' }}>
        {pcList.map((pc, index) => (
          <Card key={index} interactive>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <H5>{pc.name}</H5>
                <Text>MAC: {pc.mac}</Text>
                {pc.ip && <Text>IP: {pc.ip}</Text>}
              </div>
              <Button
                icon={Power}
                intent={Intent.SUCCESS}
                text="Wake Up"
                loading={wakingPc === pc.name}
                onClick={() => wakePc(pc)}
                disabled={wakingPc !== null}
              />
            </div>
          </Card>
        ))}
      </div>

      {/* Refresh button */}
      <div style={{ textAlign: 'center', marginTop: '20px' }}>
        <Button
          icon={Refresh}
          text="Refresh PC List"
          onClick={loadPcList}
          minimal
        />
      </div>
    </div>
  );
}

export default App; 