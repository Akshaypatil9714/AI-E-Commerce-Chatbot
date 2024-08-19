import React, { useState } from 'react';
import axios from 'axios';
import ChatInput from './ChatInput';

function Chatbox() {
  const [messages, setMessages] = useState([]);

  const sendMessage = async (message) => {
    const newMessage = { role: 'user', content: message };
    setMessages([...messages, newMessage]);

    try {
      const response = await axios.post('/api/chat/', { query: message });
      console.log("Response:", response.data.response);
      setMessages([
        ...messages,
        newMessage,
        { role: 'assistant', content: response.data.response },
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  return (
    <div className="chatbox">
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
      </div>
      <ChatInput onSend={sendMessage} />
    </div>
  );
}

export default Chatbox;
