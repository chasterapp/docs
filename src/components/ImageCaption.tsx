import React from 'react';

const ImageCaption = ({ children }) => {
  return <div style={{
    textAlign: 'center',
    marginBottom: '1rem',
  }}>
    {children}
  </div>;
};

export default ImageCaption;

