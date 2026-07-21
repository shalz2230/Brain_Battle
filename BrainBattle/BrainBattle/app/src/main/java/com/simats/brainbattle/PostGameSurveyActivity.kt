package com.simats.brainbattle

import android.os.Bundle
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.button.MaterialButton

class PostGameSurveyActivity : AppCompatActivity() {

    private lateinit var txtProgress: TextView
    private lateinit var txtQuestion: TextView
    private lateinit var btnNext: MaterialButton

    private lateinit var btnOption1: LinearLayout
    private lateinit var btnOption2: LinearLayout
    private lateinit var btnOption3: LinearLayout
    private lateinit var btnOption4: LinearLayout

    private var currentQuestionIndex = 0
    private var selectedOptionIndex = -1

    private val questions = arrayOf(
        "How is your child's confidence when solving everyday problems now?",
        "How is your child's thinking and reasoning during play activities?",
        "How is your child's confidence when completing shape puzzles now?",
        "How is your child's focus during simple learning games?",
        "How is your child's enjoyment of new learning challenges?"
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_post_game_survey)

        txtProgress = findViewById(R.id.txtProgress)
        txtQuestion = findViewById(R.id.txtQuestion)
        btnNext = findViewById(R.id.btnNext)

        btnOption1 = findViewById(R.id.btnOption1)
        btnOption2 = findViewById(R.id.btnOption2)
        btnOption3 = findViewById(R.id.btnOption3)
        btnOption4 = findViewById(R.id.btnOption4)

        setupQuestion()

        val optionsLayouts = arrayOf(btnOption1, btnOption2, btnOption3, btnOption4)
        for (i in optionsLayouts.indices) {
            optionsLayouts[i].setOnClickListener {
                selectOption(i)
            }
        }

        btnNext.setOnClickListener {
            if (currentQuestionIndex < questions.size - 1) {
                currentQuestionIndex++
                selectedOptionIndex = -1
                setupQuestion()
            } else {
                Toast.makeText(this, "Feedback saved successfully! Thank you!", Toast.LENGTH_SHORT).show()
                finish()
            }
        }
    }

    private fun setupQuestion() {
        txtProgress.text = "Question ${currentQuestionIndex + 1} of ${questions.size}"
        txtQuestion.text = questions[currentQuestionIndex]

        btnOption1.setBackgroundResource(R.drawable.card_bg)
        btnOption2.setBackgroundResource(R.drawable.card_bg)
        btnOption3.setBackgroundResource(R.drawable.card_bg)
        btnOption4.setBackgroundResource(R.drawable.card_bg)

        btnNext.isEnabled = false
    }

    private fun selectOption(index: Int) {
        selectedOptionIndex = index

        val optionsLayouts = arrayOf(btnOption1, btnOption2, btnOption3, btnOption4)
        for (i in optionsLayouts.indices) {
            if (i == index) {
                optionsLayouts[i].setBackgroundResource(R.drawable.button_gradient)
            } else {
                optionsLayouts[i].setBackgroundResource(R.drawable.card_bg)
            }
        }

        btnNext.isEnabled = true
    }
}
