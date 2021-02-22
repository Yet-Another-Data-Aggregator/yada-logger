import React from "react";
import logo from "./logo.svg";
import "./App.css";
import NetworkConnection from "./components/NetworkConnection";
import DeviceInformation from "./components/DeviceInformation";

function App() {
  // Fetches our GET route from the Express server. (Note the route we are fetching matches the GET route from server.js
  const callBackendAPI = async () => {
    const response = await fetch("/express_backend");
    const body = await response.json();

    if (response.status !== 200) {
      throw Error(body.message);
    }
    return body;
  };

  return (
    <div className="App">
      <DeviceInformation />
    </div>
  );
}

export default App;
