import { useState } from "react"
import { Link } from "react-router-dom"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import { API_URL } from "../utils/api"
import axios from "axios"

export const SignIn = () => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  })
  const navigate = useNavigate()
  const { login } = useAuth()

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await axios.post(`${API_URL}/api/v1/users/login`, formData)
      login(res.data)
      navigate('/')
    } catch (error) {
      alert("Username or password wrong!")
      console.error(error)
    }
  }
  
  return (
    <div className="h-screen flex">
      <form onSubmit={handleSubmit} className="px-6 py-8 max-w-md m-auto bg-[#f8f3ea] border-1 border-[#2625223D] shadow-md rounded-[32px]">
        <img src="/images/my_logo.png" className="w-2/7 h-2/7 mx-auto" alt="image description"/>
        <h2 className="text-[18px] font-semibold mb-2 text-start">Sign in to use application</h2>
        <input 
          type="text" 
          name="username" 
          value={formData.username}
          placeholder="Enter your username" 
          onChange={handleChange} 
          className="w-full p-2 border border-gray-300 rounded-md bg-white"
          required
        />
        <input 
          type="password" 
          name="password" 
          value={formData.password}
          placeholder="Enter your password" 
          onChange={handleChange} 
          className="w-full mt-4 p-2 border border-gray-300 rounded-md bg-white"
          required
        />
        <button type="submit" className="bg-black text-white mt-4 w-full px-4 py-2 rounded-full hover:opacity-75 cursor-pointer">Sign In</button>
        <p className="mt-4 text-center">
          Don't have an account? <Link to="/sign-up" className="font-bold hover:underline">Sign up</Link>
        </p>
      </form>
    </div>
  )
}