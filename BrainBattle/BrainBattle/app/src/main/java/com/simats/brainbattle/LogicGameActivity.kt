package com.simats.brainbattle

import android.content.Intent
import android.os.Bundle
import android.os.CountDownTimer
import android.view.Gravity
import android.widget.GridLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class LogicGameActivity : AppCompatActivity() {

    private lateinit var levelText: TextView
    private lateinit var timerText: TextView
    private lateinit var questionText: TextView
    private lateinit var grid: GridLayout

    private var level = 1
    private var time = 0

    private var correctAnswer = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.logic_game_screen)

        levelText = findViewById(R.id.levelText)
        timerText = findViewById(R.id.timerText)
        questionText = findViewById(R.id.questionText)
        grid = findViewById(R.id.optionsGrid)

        level = intent.getIntExtra("LEVEL", 1)

        levelText.text = "Level $level"

        generateQuestion()
        startTimer()
    }


    private fun generateQuestion() {

        grid.removeAllViews()

        val a = level + 1
        val b = a + 2
        val c = b + 2
        val d = c + 2

        correctAnswer = d + 2

        questionText.text = "$a  $b  $c  $d  ?"

        val options = mutableListOf(
            correctAnswer,
            correctAnswer + 2,
            correctAnswer - 2,
            correctAnswer + 4
        )

        options.shuffle()

        for (num in options) {

            val tv = TextView(this)

            val params = GridLayout.LayoutParams()
            params.width = 0
            params.height = 200
            params.columnSpec = GridLayout.spec(
                GridLayout.UNDEFINED, 1f
            )

            params.setMargins(10,10,10,10)

            tv.layoutParams = params
            tv.gravity = Gravity.CENTER
            tv.textSize = 22f
            tv.text = num.toString()

            tv.setBackgroundResource(R.drawable.box_bg)

            tv.setOnClickListener {

                if (num == correctAnswer) {
                    finishGame(3)
                } else {
                    finishGame(1)
                }

            }

            grid.addView(tv)
        }
    }


    private fun startTimer() {

        object : CountDownTimer(600000,1000){

            override fun onTick(ms: Long) {
                time++
                timerText.text = "Time $time s"
            }

            override fun onFinish() {}

        }.start()
    }


    private fun finishGame(stars:Int){

        val intent = Intent(
            this,
            ResultActivity::class.java
        )

        intent.putExtra("LEVEL", level)
        intent.putExtra("STARS", stars)
        intent.putExtra("TIME", time)

        intent.putExtra("TYPE", "logic")

        startActivity(intent)
        finish()
    }

}