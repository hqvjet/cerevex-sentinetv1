import { useState } from "react"
import { NavLink, Link } from "react-router-dom"
import { Search } from "lucide-react"
import { useAuth } from "../context/AuthContext"

export const Navbar = () => {
  const [show, setShow] = useState(false)
  const { user, logout } = useAuth()

  const linkClass = ({ isActive }) => isActive ? "font-bold text-black border-b-2 border-[#EE6352]" : ""
  const toggle = () => setShow(prev => !prev)

  return (
    <header className="flex justify-between items-center px-6 py-4 bg-[#f8f3ea] border-1 border-[#2625223D] rounded-full shadow-md shadow-[#2625223D]-500/50">
      <div className="text-xl font-semibold">
        <img src="/images/my_logo.png" className="w-10 h-10"/>
      </div>
      <nav className="hidden md:flex gap-8 uppercase text-sm text-gray-600">
        <NavLink to="/" className={linkClass}>Home</NavLink>
        <NavLink to="/create-article" className={linkClass}>Create Article</NavLink>
        <a href="#">Page 2</a>
        <a href="#">Page 3</a>
      </nav>
      <div className="flex items-center gap-4">
        <button className="p-2 rounded-2xl bg-[#26252214] shadow">
          <Search />
        </button>
        {user ? 
          <div className="relative inline-block text-left">
            <div>
              <button
                type="button"
                className="inline-flex justify-center w-full text-md font-medium text-black hover:underline cursor-pointer"
                onClick={toggle}
              >
                Hello, {user.name}
              </button>
            </div>
            {show && (
              <div className="origin-top-right absolute right-0 mt-2 w-36 rounded-xl shadow-lg bg-white z-50">
                <div className="py-1">
                  <Link
                    to="/"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    onClick={logout}
                  >
                    Logout
                  </Link>
                </div>
              </div>
            )}
          </div>
        :
        <Link to="/sign-up" className="px-4 py-2 bg-black text-white text-sm rounded-full cursor-pointer hover:opacity-75">Sign Up</Link>
        }
      </div>
    </header>
  )
}