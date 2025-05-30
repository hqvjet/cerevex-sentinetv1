import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { format } from "date-fns"
import { API_URL } from "../utils/api"
import axios from "axios"

const formatDate = (isoString) => {
  return format(new Date(isoString), "dd/MM/yyyy • HH:mm")
}

export const ArticleCard = ({ id, title, date }) => {
  const [articleTag, setArticleTag] = useState(null)
  
  useEffect(() => {
    axios
      .get(`${API_URL}/api/v1/article-tags/article/${id}`)
      .then((res) => {
        setArticleTag(res.data)
      })
      .catch((err) => {
        console.error("Lỗi khi lấy tag: ", err)
      })
  }, [])

  return (
    <div className="max-w rounded-3xl overflow-hidden bg-[#f8f3ea] border-1 border-[#2625223D] shadow-md hover:shadow-lg transition-shadow duration-300">
      <div className="p-3">
        <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
        <span className="inline-block mt-2 text-xs bg-red-200 text-red-700 px-3 py-1 rounded-full uppercase tracking-wide">
          {articleTag?.[0]?.name || "undefind"}
        </span>
        <div className="flex justify-between mt-2">
          <p className="text-xs text-gray-500 mt-2">{formatDate(date)}</p>
          <Link
            to={`/view-article/${id}`}
            className="text-sm px-4 py-1 border border-gray-400 rounded-full hover:bg-gray-100"
          >
            View
          </Link>
        </div>
      </div>
    </div>
  )
}
