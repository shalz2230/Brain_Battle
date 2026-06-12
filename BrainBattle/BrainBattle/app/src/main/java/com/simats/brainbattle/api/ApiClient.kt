package com.simats.brainbattle.api

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object ApiClient {

    private const val BASE_URL = "http://10.197.170.23:5000/"
    // ⚠️ IMPORTANT:
    // 10.0.2.2 = localhost (for emulator)
    // If using real phone, use your PC IP

    val instance: ApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}