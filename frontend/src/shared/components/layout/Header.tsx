import { useState, useEffect, useRef } from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../../../features/auth/hooks/useAuth";

const Header = () => {
  const { user, signOut } = useAuth();

  const isAuthenticated = !!user;

  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const location = useLocation();

  const isLoginPage = location.pathname === "/login";
  const isSignupPage = location.pathname === "/signup";

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [isOpen]);

  return (
    <header className="bg-gray-800 text-white p-4 flex justify-between items-center">
      <h1 className="text-lg font-bold">Running App</h1>

      <nav className="relative flex items-center gap-4">
        {isAuthenticated ? (
          <>
            <Link to="/dashboard">ダッシュボード</Link>

            <div className="relative" ref={dropdownRef}>
              <button
                onClick={() => setIsOpen(!isOpen)}
                className="bg-gray-700 px-4 py-2 rounded"
              >
                {user?.email}
              </button>

              {isOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-white text-black rounded shadow-lg">
                  <Link to="/profile" className="block px-4 py-2 hover:bg-gray-200">
                    プロフィール
                  </Link>

                  <button
                    onClick={signOut}
                    className="block w-full text-left px-4 py-2 hover:bg-gray-200"
                  >
                    ログアウト
                  </button>
                </div>
              )}
            </div>
          </>
        ) : (
          <>
            {isLoginPage && <Link to="/signup">新規登録</Link>}
            {isSignupPage && <Link to="/login">ログイン</Link>}
          </>
        )}
      </nav>
    </header>
  );
};

export default Header;