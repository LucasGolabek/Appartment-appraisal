import { Modal, useModal, ModalTransition } from "react-simple-hook-modal";
import React from "react";

export const MyComponent = () => {
  const { isModalOpen, openModal, closeModal } = useModal();

  return (
    <>
      <button onClick={openModal}>Open</button>
      <Modal
        id="any-unique-identifier"
        isOpen={isModalOpen}
        transition={ModalTransition.BOTTOM_UP}
      >
        <button onClick={openModal}>Open</button>
      </Modal>
    </>
  );
};
