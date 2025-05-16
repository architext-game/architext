import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Icon } from "@iconify/react";

interface HamburguerMenuProps {
  children: React.ReactNode;
}

export const HamburgerMenu = ({ children }: HamburguerMenuProps) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Icono de Hamburguesa con Animación */}
      <button
        className="fixed top-4 left-4 z-50 p-2 text-white opacity-70 hover:opacity-100 rounded-full"
        onClick={() => setIsOpen(!isOpen)}
      >
        <motion.div
          key={isOpen ? "close" : "menu"}
          initial={{ rotate: 0, opacity: 0 }}
          animate={{ rotate: isOpen ? 180 : 0, opacity: 1 }}
          exit={{ rotate: 0, opacity: 0 }}
          transition={{ duration: 0.3 }}
        >
          <Icon
            icon={isOpen ? "mdi:close" : "mdi:menu"}
            width="32"
            height="32"
          />
        </motion.div>
      </button>

      {/* Menú Desplegable con Animación */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0.5, x: -100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0.5, x: -100 }}
            transition={{ duration: 0.3 }}
            className="fixed top-0 left-0 w-fit h-full bg-black/10 backdrop-blur-lg text-white z-40 flex flex-col px-8 pt-20"
          >
            { children }
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};
