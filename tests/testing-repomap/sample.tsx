import React, { useState, useEffect } from 'react';

interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

class ErrorBoundary extends React.Component<{ children: React.ReactNode }> {
  state = { hasError: false };

  componentDidCatch(error: Error) {
    console.error(error);
  }

  render() {
    return this.state.hasError ? <div>Error</div> : this.props.children;
  }
}

function Button({ label, onClick, disabled = false }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
}

const Modal = ({ children, isOpen }: { children: React.ReactNode; isOpen: boolean }) => {
  const [visible, setVisible] = useState(isOpen);
  useEffect(() => setVisible(isOpen), [isOpen]);
  return visible ? <div className="modal">{children}</div> : null;
};

export { Button, Modal, ErrorBoundary };
