// src/contexts/AudioContext.tsx
import React, { createContext, useState, useContext } from "react";

const AudioContext = createContext(null);

export const AudioProvider = ({ children }) => {
  const [audioFile, setAudioFile] = useState(null);

  return (
    <AudioContext.Provider value={{ audioFile, setAudioFile }}>
      {children}
    </AudioContext.Provider>
  );
};

export const useAudioContext = () => useContext(AudioContext);
