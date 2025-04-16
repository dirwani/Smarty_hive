import Home from "../pages/Home/home";
import Login from "../pages/Login/login";
import Register from "../pages/Register/register";
import NotFound from "../pages/NotFound/notFound";
import { Routes, Route } from "react-router-dom";
import ProtectedRoute from "../components/Common/ProtectedRoute/ProtectedRoute";
import PublicRoute from "../components/Common/PublicRoute/PublicRoute";
import { ChangePassword } from "../pages/ChangePassword/changePassword";
import ForgotPassword from "../pages/ForgotPassword/forgotPassword";
import { ResetPassword } from "../pages/ResetPassword/resetPassword";
import DetailPage from "../pages/DetailPage/detailPage";
import CreatePost from "../pages/CreatePost/post";
import SemesterFilter from "../pages/Semester/semester";
import SearchFilter from "../pages/SearchPage/serachPage";
import { Structure } from "../layout/structure";
import { Assignment } from "../pages/Assignment/assignment";


function RegisterAndLogout() {
    localStorage.clear()
    return <Register />;
}


// ! Projects Route Layout 
export default function RouteLayout() {
    return (
        <div>
            <Routes>
                <Route path="/" element={
                    <ProtectedRoute>
                        <Structure />
                    </ProtectedRoute>
                }>
                    <Route path="" element={<Home />} />
                    <Route path="/semester/:semester" element={<SemesterFilter />} />
                    <Route path="/assignments" element={<Assignment/>} />
                </Route>

                <Route path="/question/:id" element={<ProtectedRoute> <DetailPage /> </ProtectedRoute>} />
                <Route path="/ask-question" element={<ProtectedRoute> <CreatePost /> </ProtectedRoute>} />
                <Route path="/search/:str" element={<ProtectedRoute> <SearchFilter /> </ProtectedRoute>} />
                <Route path="/change-password" element={<ProtectedRoute><ChangePassword />   </ProtectedRoute>} />

                <Route path="/login" element={
                    <PublicRoute>
                        <Login />
                    </PublicRoute>}
                />

                <Route path="/register" element={
                    <PublicRoute>
                        <RegisterAndLogout />
                    </PublicRoute>
                } />

                <Route path="/forgot-password" element={
                    <PublicRoute>
                        <ForgotPassword />
                    </PublicRoute>
                } />

                <Route path="/reset-password/:uid/:token" element={
                    <PublicRoute>
                        <ResetPassword />
                    </PublicRoute>
                } />

                {/* ! If the Route Other than the specified one are mapped this NotFound Component Will be Called */}
                <Route path="*" element={<NotFound />} />
            </Routes>
        </div >
    )
}