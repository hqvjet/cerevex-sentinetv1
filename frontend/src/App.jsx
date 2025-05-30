import { Route, Routes } from "react-router-dom"
import { Home } from "./pages/Home"
import { CreateArticle } from "./pages/CreateArticle"
import { ArticleDetail } from "./pages/ArticleDetail"
import { SignUp } from "./pages/SignUp"
import { SignIn } from "./pages/SignIn"
import { Navbar } from "./components/Navbar"
import { useLocation } from "react-router-dom"

function App() {
  const location = useLocation()
  const hiddenNavbar = ["/sign-up", "/sign-in"].includes(location.pathname)

  return (
    <div className={`${hiddenNavbar ? "" : "px-10 py-4"}`}>
      {!hiddenNavbar && <Navbar/>}
      <Routes>
        <Route index element={<Home/>}/>
        <Route path="/create-article" element={<CreateArticle/>}/>
        <Route path="/view-article/:articleId" element={<ArticleDetail/>}/>
        <Route path="/sign-up" element={<SignUp/>}/>
        <Route path="/sign-in" element={<SignIn/>}/>
      </Routes>
    </div>
  )
}

export default App
