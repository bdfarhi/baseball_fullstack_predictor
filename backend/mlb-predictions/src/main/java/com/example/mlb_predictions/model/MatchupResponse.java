package com.example.mlb_predictions.model;

public class MatchupResponse {
    private String winner;

    public MatchupResponse() {
    }

    public MatchupResponse(String winner) {
        this.winner = winner;
    }

    public String getWinner() {
        return winner;
    }

    public void setWinner(String winner) {
        this.winner = winner;
    }
}
