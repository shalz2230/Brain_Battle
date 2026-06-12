package com.simats.brainbattle.api

import retrofit2.Call
import retrofit2.http.*

data class AuthRequest(
    val username: String? = null,
    val email: String,
    val password: String
)

data class LoginResponse(
    val status: String,
    val message: String,
    val username: String,
    val email: String
)

data class SimpleResponse(
    val status: String,
    val message: String
)

data class UserRequest(val email: String)

data class UserResponse(
    val status: String,
    val username: String
)

data class ProgressRequest(
    val email: String,
    val game_type: String,
    val level: Int,
    val stars: Int,
    val time_taken: Int
)

data class ProgressItem(
    val level: Int,
    val stars: Int,

    val completed: Boolean
)

data class DashboardResponse(
    val current_level: Int,
    val total_stars: Int,
    val last_game: String,
    val rank: Int,
    val levels_completed: Int
)

data class ChangePasswordRequest(
    val email: String,
    val password: String
)

data class MessageResponse(
    val status: String,
    val message: String
)



interface ApiService {

    @POST("api/auth/signup")
    fun signup(@Body request: AuthRequest): Call<SimpleResponse>

    @POST("api/auth/login")
    fun login(@Body request: AuthRequest): Call<LoginResponse>

    @POST("api/user/get-user")
    fun getUser(@Body request: UserRequest): Call<UserResponse>

    @POST("api/progress/save")
    fun saveProgress(
        @Body request: ProgressRequest
    ): Call<SimpleResponse>


    @GET("api/progress/get/{email}/{game}")
    fun getProgress(
        @Path("email") email: String,
        @Path("game") game: String
    ): Call<List<ProgressItem>>

    @GET("api/dashboard/{email}")
    fun getDashboard(
        @Path("email") email: String
    ): Call<DashboardResponse>

    @POST("api/user/forgot-password")
    fun forgotPassword(
        @Body request: UserRequest
    ): Call<MessageResponse>

    @POST("api/user/change-password")
    fun changePassword(
        @Body request: ChangePasswordRequest
    ): Call<MessageResponse>
}