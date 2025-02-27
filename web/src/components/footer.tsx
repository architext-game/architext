export const Footer = () => {
  return (
    <footer className="w-full text-white py-6">
      <div className="max-w-5xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
        
        {/* Logo y Copyright */}
        <div className="flex items-center space-x-2">
          {/* <img 
            src="https://img.icons8.com/ios-filled/50/FFFFFF/cube.png" 
            alt="Logo" 
            className="w-6 h-6"
          /> */}
          <a href="#"  className="font-bold text-lg hover:underline">Architext</a>
        </div>
        
        {/* <p className="text-gray-400 text-sm">© 2024 Architext</p> */}
        
        {/* Menú de Navegación */}
        <ul className="flex space-x-6 text-sm">
          <li><a href="/#" className="hover:underline">Home</a></li>
          <li><a href="/worlds" className="hover:underline">Play</a></li>
          <li><a href="/#faq" className="hover:underline">FAQ</a></li>
          {/* <li><a href="#" className="hover:underline">Contact</a></li> */}
        </ul>
      </div>
    </footer>
  );
};
