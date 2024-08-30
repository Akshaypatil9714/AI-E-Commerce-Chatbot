import React, { useState } from 'react';
import axios from 'axios';
import ChatInput from './ChatInput';

function Chatbox() {
  const [messages, setMessages] = useState([]);

  // Set the API base URL based on the environment variable or default to localhost for local development
  const API_BASE_URL = process.env.REACT_APP_NODEJS_API_URL || 'http://localhost:3001';

  const sendMessage = async (message) => {
    const newMessage = { role: 'user', content: message };
    setMessages([...messages, newMessage]);

    try {
      // Use the dynamically determined API base URL
      const response = await axios.post(`${API_BASE_URL}/api/chat/`, { query: message });
      console.log("Response:", response.data.response);
      console.log("Retrieved Documents:", response.data.retrieved_docs); // Log retrieved content

      setMessages((prevMessages) => [
        ...prevMessages,
        newMessage,
        { role: 'assistant', content: response.data.response },
        { role: 'system', content: JSON.stringify(response.data.retrieved_docs, null, 2) }, // Optional: Show retrieved docs
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { role: 'assistant', content: "Sorry, something went wrong. Please try again." },
      ]);
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
