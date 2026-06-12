package com.simats.brainbattle

import android.content.Intent
import android.os.Bundle
import android.view.animation.Animation
import android.view.animation.AnimationUtils
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class SplashActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash)

        val logo = findViewById<ImageView>(R.id.logo)
        val slogan = findViewById<TextView>(R.id.slogan)

        val zoomRotate = AnimationUtils.loadAnimation(this, R.anim.zoom_rotate)
        val bounce = AnimationUtils.loadAnimation(this, R.anim.bounce)
        val fadeIn = AnimationUtils.loadAnimation(this, R.anim.fade_in)

        // start first animation
        logo.startAnimation(zoomRotate)

        zoomRotate.setAnimationListener(object : Animation.AnimationListener {

            override fun onAnimationStart(animation: Animation?) {}

            override fun onAnimationEnd(animation: Animation?) {

                logo.startAnimation(bounce)
                slogan.startAnimation(fadeIn)

                fadeIn.setAnimationListener(object : Animation.AnimationListener {

                    override fun onAnimationStart(animation: Animation?) {}

                    override fun onAnimationEnd(animation: Animation?) {

                        startActivity(
                            Intent(
                                this@SplashActivity,
                                LoginActivity::class.java
                            )
                        )
                        finish()

                    }

                    override fun onAnimationRepeat(animation: Animation?) {}
                })
            }

            override fun onAnimationRepeat(animation: Animation?) {}
        })
    }
}