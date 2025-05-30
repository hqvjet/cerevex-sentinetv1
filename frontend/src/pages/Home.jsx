import { useEffect, useState } from "react"
import { ArticleCard } from "../components/ArticleCard"
import { API_URL } from "../utils/api"
import axios from "axios"

export const Home = () => {
  const [articles, setArticles] = useState([])
  const [connect, setConnect] = useState(true)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    axios
      .get(`${API_URL}/api/v1/articles/all`)
      .then((res) => {
        setArticles(res.data)
        setLoading(false)
      })
      .catch((err) => {
        console.error("Lỗi khi lấy danh sách bài viết:", err)
        setLoading(false)
        setConnect(false)
      })
  }, [])

  if (loading) {
    return <div className="min-h-screen px-6 py-8">
      <div role="status" className="max-w-5xl mx-auto grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 animate-pulse">
        <div class="max-w-xs h-80 bg-gray-200 rounded-3xl overflow-hidden dark:bg-gray-700"></div>
        <div class="max-w-xs h-80 bg-gray-200 rounded-3xl overflow-hidden dark:bg-gray-700"></div>
        <div class="max-w-xs h-80 bg-gray-200 rounded-3xl overflow-hidden dark:bg-gray-700"></div>
      </div>
    </div>
  }

  if (!articles) return <div className="text-center mt-4 text-red-500">Articles not found.</div>

  if (!connect) return <div className="text-center mt-4 text-red-500">Disconnect to server.</div>

  return (
    <div className="min-h-screen px-6 py-8">
      <div className="max-w-5xl mx-auto grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {articles.map((article) => (
          <ArticleCard
            key={article.id}
            id={article.id}
            title={article.title}
            date={article.created_at}
          />
        ))}
      </div> 
    </div>
  )
}