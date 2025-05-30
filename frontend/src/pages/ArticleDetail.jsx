import { useState, useEffect, useRef } from "react"
import { Clock12 } from "lucide-react"
import { useParams } from "react-router-dom"
import { API_URL } from "../utils/api"
import { format } from "date-fns"
import { useAuth } from "../context/AuthContext"
import { Link } from "react-router-dom"
import { ThumbsUp } from 'lucide-react'
import { ThumbsDown } from 'lucide-react'
import axios from "axios"

const formatDate = (isoString) => {
  return format(new Date(isoString), "dd/MM/yyyy • HH:mm")
}

export const ArticleDetail = () => {
  const { articleId } = useParams()
  const { user } = useAuth()
  const [article, setArticle] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showFeedback, setShowFeedback] = useState(false)
  const [feedback, setFeedback] = useState("")
  const [show, setShow] = useState(false)
  const dropdownRef = useRef(null)

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        const res = await axios.get(`${API_URL}/api/v1/articles/get/${articleId}`)
        setArticle(res.data)
        setLoading(false)
      } catch (error) {
        console.error("Lỗi khi lấy thông tin bài báo:", error)
        setLoading(false)
      }
    }

    fetchArticle()
  }, [articleId])

  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShow(false)
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
    }
  }, [])

  const handleToggleFeedback = () => {
    setShowFeedback((prev) => !prev)
  }

  const handleSubmitFeedback = () => {
    alert(`Feedback đã gửi: ${feedback}`)
    setFeedback("")
    setShowFeedback(false)
  }

  const toggle = () => setShow(prev => !prev)

  if (loading) {
    return <div className="min-h-screen px-6 py-8">
      <div role="status" className="max-w-5xl mx-auto animate-pulse">
        <div class="h-96 bg-gray-200 rounded-3xl overflow-hidden dark:bg-gray-700"></div>
      </div>
    </div>
  }

  if (!user) return <div className="flex items-center justify-center mt-10">
    <div className="w-full max-w-md text-center px-4">
      <p className="text-red-600 text-lg mb-4">Please sign in to view article!</p>
      <Link
        to="/sign-in"
        className="bg-black text-white text-sm px-6 py-2 rounded-full hover:opacity-75"
      >
        Sign In
      </Link>
    </div>
  </div>

  return (
    <div className="min-h-screen px-6 py-8">
      <div className="max-w-5xl mx-auto bg-[#f8f3ea] rounded-[32px] border-1 border-[#2625223D] shadow-md p-6">
        <div className="text-center mb-4">
          <span className="bg-red-500 text-white text-xs px-3 py-1 rounded-full uppercase tracking-wide">
            {article.tag || "undefind"}
          </span>
          <h1 className="text-3xl md:text-4xl font-bold mt-4 uppercase">
            {article.title}
          </h1>
          <p className="flex items-center justify-center text-sm text-gray-500 mt-2">
            <Clock12 className="me-2"/> {formatDate(article.created_at)}
          </p>
        </div>

        <div className="space-y-4 text-gray-700 leading-relaxed text-sm">
          <p>
            {article.content}
          </p>
        </div>

        <div className="flex items-center gap-4 mt-8 border-t pt-6">
          <img
            src="https://randomuser.me/api/portraits/women/44.jpg"
            alt="Author"
            className="w-12 h-12 rounded-full"
          />
          <div>
            <h4 className="font-semibold text-sm">Isabella Russo</h4>
            <p className="text-xs text-gray-500">
              A writer with a pinch of zest and passion...
            </p>
          </div>
        </div>

        <div className="flex flex-col md:flex-row items-center justify-between mt-6">
          <button className="mt-4 md:mt-0 bg-white border text-sm border-gray-300 px-6 py-2 rounded-full hover:bg-gray-100">
            Read More
          </button>
          <div className="flex space-x-2">
            <button className="inline-flex items-center justify-center w-10 h-10 rounded-full border-1 border-[#2625223D] bg-[#e9e9e980] hover:opacity-75 transition duration-200 cursor-pointer">
              <ThumbsUp className="text-gray-700 w-5 h-5"/>
            </button>
            <div className="relative inline-block text-left" ref={dropdownRef}>
              {/* Button trigger */}
              <button
                type="button"
                onClick={toggle}
                className="inline-flex items-center justify-center w-10 h-10 rounded-full border-1 border-[#2625223D] bg-[#e9e9e980] hover:opacity-75 transition duration-200 cursor-pointer"
                title="Reactions"
              >
                <ThumbsDown className="text-gray-700 w-5 h-5"/>
              </button>

              {/* Dropdown content */}
              {show && (
                <div className="origin-top-right absolute right-0 mt-2 w-40 rounded-xl shadow-lg bg-white ring-1 ring-black/5 z-50 animate-fade-in">
                  <div className="py-1">
                    <Link
                      to="/"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md transition-colors duration-150"
                    >
                      #TagName
                    </Link>
                  </div>
                </div>
              )}
            </div>
            <button 
              className="mt-4 md:mt-0 bg-black text-white text-sm px-6 py-2 rounded-full hover:opacity-75"
              onClick={handleToggleFeedback}
            >
              Comment
            </button>
          </div>
        </div>

        {showFeedback && (
          <div className="mt-6">
            <textarea
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              rows={4}
              placeholder="Enter your comment..."
              className="w-full bg-white border border-gray-300 rounded-xl p-3 text-sm focus:ring-black"
            />
            <button
              onClick={handleSubmitFeedback}
              className="mt-2 bg-blue-700 text-white text-sm px-4 py-2 rounded-full hover:opacity-75 cursor-pointer"
            >
              Submit
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
