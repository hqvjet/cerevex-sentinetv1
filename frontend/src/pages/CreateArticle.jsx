import { useState, useEffect } from "react"
import { API_URL } from "../utils/api"
import { useAuth } from "../context/AuthContext"
import { Link } from "react-router-dom"
import axios from "axios"

export const CreateArticle = () => {
  const { user } = useAuth()
  const [formData, setFormData] = useState({
    user_id: "",
    tag: "",
    title: "",
    content: "",
  })
  const [message, setMessage] = useState("")
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (user) {
      setFormData((prev) => ({ ...prev, user_id: user.id }))
    }
  }, [user])

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage("")
    
    try {
      const response = await axios.post(`${API_URL}/api/v1/articles/create`, formData)
      setMessage("✅ Bài viết đã được tạo thành công!")
      setFormData({ user_id: user.id, tag: "", title: "", content: "" })
    } catch (error) {
      console.error(error);
      setMessage("Đã có lỗi xảy ra khi tạo bài viết.")
    } finally {
      setLoading(false)
    }
  }

  if (!user) return <div className="flex items-center justify-center mt-10">
    <div className="w-full max-w-md text-center px-4">
      <p className="text-red-600 text-lg mb-4">Please sign in to create article!</p>
      <Link
        to="/sign-in"
        className="bg-black text-white text-sm px-6 py-2 rounded-full hover:opacity-75"
      >
        Sign In
      </Link>
    </div>
  </div>

  return (
    <div className="max-w-3xl mx-auto p-6 bg-[#f8f3ea] border-1 border-[#2625223D] shadow-md rounded-[32px] mt-8">
      <h2 className="text-3xl font-bold mb-4">Create New Article</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium">Title</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            className="w-full mt-1 p-2 border border-gray-300 rounded-md bg-white"
            placeholder="Enter title"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium">Content</label>
          <textarea
            rows="6"
            name="content"
            value={formData.content}
            onChange={handleChange}
            className="w-full mt-1 p-2 border border-gray-300 rounded-md bg-white"
            placeholder="Enter content"
            required
          />
        </div>
        <button
          type="submit"
          className="bg-black text-white px-4 py-2 rounded-full hover:opacity-75 cursor-pointer"
        >
          {loading ? "Đang gửi..." : "Create Article"}
        </button>
        {message && (
          <div
            className={`text-md font-medium ${
              message.startsWith("✅") ? "text-green-600" : "text-red-600"
            }`}
          >
            {message}
          </div>
        )}
      </form>
    </div>
  )
}
