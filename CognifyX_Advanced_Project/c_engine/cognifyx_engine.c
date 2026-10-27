/*
 * CognifyX C Decision Engine
 * Educational demo: scoring, accuracy, and simple adaptive difficulty.
 * Compile: gcc -std=c11 -O2 cognifyx_engine.c -o cognifyx_engine
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int parse_int(const char *s, int *out) {
    char *end = NULL;
    long value;
    if (!s || !*s) return 0;
    value = strtol(s, &end, 10);
    if (*end != '\0' || value < -1000000 || value > 1000000) return 0;
    *out = (int)value;
    return 1;
}

static int clamp_int(int x, int lo, int hi) {
    return x < lo ? lo : (x > hi ? hi : x);
}

static int score_command(int argc, char **argv) {
    int correct, wrong, skipped, seconds, total;
    int score, max_score;
    double accuracy, percentage;
    if (argc < 7 || !parse_int(argv[2], &correct) || !parse_int(argv[3], &wrong) ||
        !parse_int(argv[4], &skipped) || !parse_int(argv[5], &seconds) ||
        !parse_int(argv[6], &total)) {
        fprintf(stderr, "Usage: cognifyx_engine score <correct> <wrong> <skipped> <seconds> <total>\n");
        return 2;
    }
    if (correct < 0 || wrong < 0 || skipped < 0 || seconds < 0 || total < 1 ||
        correct + wrong + skipped != total) {
        fprintf(stderr, "Invalid counts: correct + wrong + skipped must equal total.\n");
        return 2;
    }
    score = correct * 4 - wrong;
    max_score = total * 4;
    accuracy = (correct + wrong) > 0 ? (100.0 * correct / (correct + wrong)) : 0.0;
    percentage = 100.0 * score / max_score;
    if (percentage < 0.0) percentage = 0.0;
    if (percentage > 100.0) percentage = 100.0;
    printf("{\"correct\":%d,\"wrong\":%d,\"skipped\":%d,\"total\":%d,\"seconds\":%d,\"score\":%d,\"max_score\":%d,\"accuracy\":%.2f,\"percentage\":%.2f}\n",
           correct, wrong, skipped, total, seconds, score, max_score, accuracy, percentage);
    return 0;
}

static int adapt_command(int argc, char **argv) {
    int level, correct, next;
    if (argc < 4 || !parse_int(argv[2], &level) || !parse_int(argv[3], &correct)) {
        fprintf(stderr, "Usage: cognifyx_engine adapt <current_level_1_to_3> <correct_0_or_1>\n");
        return 2;
    }
    if (level < 1 || level > 3 || (correct != 0 && correct != 1)) {
        fprintf(stderr, "Level must be 1..3 and correct must be 0 or 1.\n");
        return 2;
    }
    next = clamp_int(level + (correct ? 1 : -1), 1, 3);
    printf("{\"current_level\":%d,\"correct\":%d,\"next_level\":%d,\"difficulty\":\"%s\"}\n",
           level, correct, next, next == 1 ? "Easy" : (next == 2 ? "Medium" : "Hard"));
    return 0;
}

static int recommend_command(int argc, char **argv) {
    int scores[4], i, weakest = 0;
    const char *names[] = {"Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "Computer Fundamentals"};
    const char *actions[] = {"Practice percentages, ratios, rates, and time-and-work questions.",
                             "Practice sequences, pattern recognition, and logical deductions.",
                             "Review grammar, vocabulary, and concise sentence construction.",
                             "Revise data structures, algorithms, memory, and C fundamentals."};
    if (argc < 6) {
        fprintf(stderr, "Usage: cognifyx_engine recommend <quant_0_100> <logic_0_100> <verbal_0_100> <computer_0_100>\n");
        return 2;
    }
    for (i = 0; i < 4; ++i) {
        if (!parse_int(argv[i + 2], &scores[i]) || scores[i] < 0 || scores[i] > 100) {
            fprintf(stderr, "Category scores must be integers between 0 and 100.\n");
            return 2;
        }
        if (scores[i] < scores[weakest]) weakest = i;
    }
    printf("{\"weakest_category\":\"%s\",\"score\":%d,\"recommendation\":\"%s\"}\n",
           names[weakest], scores[weakest], actions[weakest]);
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        puts("CognifyX C Decision Engine\nCommands: score, adapt, recommend");
        return 0;
    }
    if (strcmp(argv[1], "score") == 0) return score_command(argc, argv);
    if (strcmp(argv[1], "adapt") == 0) return adapt_command(argc, argv);
    if (strcmp(argv[1], "recommend") == 0) return recommend_command(argc, argv);
    fprintf(stderr, "Unknown command. Use score, adapt, or recommend.\n");
    return 2;
}
