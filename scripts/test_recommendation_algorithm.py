#!/usr/bin/env python3
"""
Test the recommendation algorithm with known inputs.

Tests:
- Match score calculation
- Penalty logic (too easy/hard books)
- Reading level bonus
- Edge cases
"""
import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

# Add backend directory to path for imports
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from generate_recommendations import calculate_match_score


def test_match_score_calculation():
    """Test match score calculation with known inputs."""
    print("=" * 70)
    print("TEST 2.1: Match Score Calculation")
    print("=" * 70)
    
    all_passed = True
    
    # Test 1: Perfect match (50% known, same reading level)
    print("\n1. Testing perfect match (50% known, same reading level)...")
    score = calculate_match_score(
        known_percent=0.5,
        book_reading_level=7.0,
        student_reading_level=7.0
    )
    print(f"   Known: 50%, Reading level diff: 0.0")
    print(f"   Match score: {score:.3f}")
    if score > 0.8:  # Should be high for perfect match
        print("   ✅ Score is high (expected for perfect match)")
    else:
        print(f"   ⚠️  Score is lower than expected: {score:.3f}")
        all_passed = False
    
    # Test 2: Too easy (90% known)
    print("\n2. Testing too easy book (90% known)...")
    score = calculate_match_score(
        known_percent=0.9,
        book_reading_level=7.0,
        student_reading_level=7.0
    )
    print(f"   Known: 90%, Reading level diff: 0.0")
    print(f"   Match score: {score:.3f}")
    if score < 0.5:  # Should be penalized
        print("   ✅ Score is penalized (expected for too easy)")
    else:
        print(f"   ⚠️  Score should be lower for too easy book: {score:.3f}")
        all_passed = False
    
    # Test 3: Too hard (20% known)
    print("\n3. Testing too hard book (20% known)...")
    score = calculate_match_score(
        known_percent=0.2,
        book_reading_level=7.0,
        student_reading_level=7.0
    )
    print(f"   Known: 20%, Reading level diff: 0.0")
    print(f"   Match score: {score:.3f}")
    if score < 0.5:  # Should be penalized
        print("   ✅ Score is penalized (expected for too hard)")
    else:
        print(f"   ⚠️  Score should be lower for too hard book: {score:.3f}")
        all_passed = False
    
    # Test 4: Reading level mismatch (2 grades difference)
    print("\n4. Testing reading level mismatch (2 grades difference)...")
    score = calculate_match_score(
        known_percent=0.5,
        book_reading_level=9.0,
        student_reading_level=7.0
    )
    print(f"   Known: 50%, Reading level diff: 2.0")
    print(f"   Match score: {score:.3f}")
    score_same_level = calculate_match_score(
        known_percent=0.5,
        book_reading_level=7.0,
        student_reading_level=7.0
    )
    if score < score_same_level:  # Should be lower than same level
        print(f"   ✅ Score is lower with level mismatch ({score:.3f} < {score_same_level:.3f})")
    else:
        print(f"   ⚠️  Score should be lower with level mismatch")
        all_passed = False
    
    # Test 5: Reading level match (1 grade difference - acceptable)
    print("\n5. Testing reading level match (1 grade difference)...")
    score = calculate_match_score(
        known_percent=0.5,
        book_reading_level=8.0,
        student_reading_level=7.0
    )
    print(f"   Known: 50%, Reading level diff: 1.0")
    print(f"   Match score: {score:.3f}")
    if score > 0.6:  # Should still be good
        print("   ✅ Score is good (expected for ±1 grade)")
    else:
        print(f"   ⚠️  Score might be too low: {score:.3f}")
        all_passed = False
    
    # Test 6: Edge case - 0% known
    print("\n6. Testing edge case: 0% known...")
    score = calculate_match_score(
        known_percent=0.0,
        book_reading_level=7.0,
        student_reading_level=7.0
    )
    print(f"   Known: 0%, Reading level diff: 0.0")
    print(f"   Match score: {score:.3f}")
    if 0 <= score <= 1:  # Should be in valid range
        print("   ✅ Score is in valid range [0, 1]")
    else:
        print(f"   ❌ Score out of range: {score:.3f}")
        all_passed = False
    
    # Test 7: Edge case - 100% known
    print("\n7. Testing edge case: 100% known...")
    score = calculate_match_score(
        known_percent=1.0,
        book_reading_level=7.0,
        student_reading_level=7.0
    )
    print(f"   Known: 100%, Reading level diff: 0.0")
    print(f"   Match score: {score:.3f}")
    if 0 <= score <= 1:  # Should be in valid range
        print("   ✅ Score is in valid range [0, 1]")
        if score < 0.5:  # Should be penalized
            print("   ✅ Score is penalized (expected for too easy)")
        else:
            print(f"   ⚠️  Score might be too high for 100% known: {score:.3f}")
    else:
        print(f"   ❌ Score out of range: {score:.3f}")
        all_passed = False
    
    # Test 8: Edge case - no reading level
    print("\n8. Testing edge case: book with no reading level...")
    score = calculate_match_score(
        known_percent=0.5,
        book_reading_level=None,
        student_reading_level=7.0
    )
    print(f"   Known: 50%, Reading level: None")
    print(f"   Match score: {score:.3f}")
    if 0 <= score <= 1:  # Should be in valid range
        print("   ✅ Score is in valid range [0, 1]")
    else:
        print(f"   ❌ Score out of range: {score:.3f}")
        all_passed = False
    
    # Test 9: Optimal range (40-60% known)
    print("\n9. Testing optimal range (40-60% known)...")
    scores = []
    for known_pct in [0.4, 0.45, 0.5, 0.55, 0.6]:
        score = calculate_match_score(
            known_percent=known_pct,
            book_reading_level=7.0,
            student_reading_level=7.0
        )
        scores.append((known_pct, score))
        print(f"   Known: {known_pct:.0%}, Score: {score:.3f}")
    
    # Check that scores are relatively high in this range
    avg_score = sum(s for _, s in scores) / len(scores)
    if avg_score > 0.6:
        print(f"   ✅ Average score in optimal range is good: {avg_score:.3f}")
    else:
        print(f"   ⚠️  Average score might be too low: {avg_score:.3f}")
        all_passed = False
    
    # Test 10: Verify score is always in [0, 1] range
    print("\n10. Testing score clamping to [0, 1] range...")
    test_cases = [
        (0.0, 7.0, 7.0),
        (0.3, 7.0, 7.0),
        (0.5, 7.0, 7.0),
        (0.8, 7.0, 7.0),
        (1.0, 7.0, 7.0),
        (0.5, 5.0, 7.0),
        (0.5, 10.0, 7.0),
    ]
    all_in_range = True
    for known_pct, book_level, student_level in test_cases:
        score = calculate_match_score(known_pct, book_level, student_level)
        if not (0 <= score <= 1):
            print(f"   ❌ Score out of range: {score:.3f} (known={known_pct:.0%}, book={book_level}, student={student_level})")
            all_in_range = False
    
    if all_in_range:
        print("   ✅ All scores are in valid range [0, 1]")
    else:
        all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL MATCH SCORE CALCULATION TESTS PASSED")
    else:
        print("⚠️  SOME TESTS HAD WARNINGS (algorithm may need tuning)")
    print("=" * 70)
    
    return all_passed


def test_penalty_logic():
    """Test penalty logic for too easy/hard books."""
    print("\n" + "=" * 70)
    print("TEST 2.2: Penalty Logic")
    print("=" * 70)
    
    all_passed = True
    
    # Test penalty for too easy (>80% known)
    print("\n1. Testing penalty for too easy books (>80% known)...")
    easy_scores = []
    for known_pct in [0.81, 0.85, 0.9, 0.95, 1.0]:
        score = calculate_match_score(
            known_percent=known_pct,
            book_reading_level=7.0,
            student_reading_level=7.0
        )
        easy_scores.append((known_pct, score))
        print(f"   Known: {known_pct:.0%}, Score: {score:.3f}")
    
    # Check that scores decrease as known percent increases above 80%
    decreasing = all(
        easy_scores[i][1] >= easy_scores[i+1][1]
        for i in range(len(easy_scores) - 1)
    )
    if decreasing:
        print("   ✅ Scores decrease as known percent increases (penalty working)")
    else:
        print("   ⚠️  Penalty may not be strong enough")
        all_passed = False
    
    # Test penalty for too hard (<30% known)
    print("\n2. Testing penalty for too hard books (<30% known)...")
    hard_scores = []
    for known_pct in [0.0, 0.1, 0.2, 0.25, 0.29]:
        score = calculate_match_score(
            known_percent=known_pct,
            book_reading_level=7.0,
            student_reading_level=7.0
        )
        hard_scores.append((known_pct, score))
        print(f"   Known: {known_pct:.0%}, Score: {score:.3f}")
    
    # Check that scores increase as known percent increases (less penalty)
    increasing = all(
        hard_scores[i][1] <= hard_scores[i+1][1]
        for i in range(len(hard_scores) - 1)
    )
    if increasing:
        print("   ✅ Scores increase as known percent increases (penalty decreasing)")
    else:
        print("   ⚠️  Penalty behavior may need adjustment")
        all_passed = False
    
    # Test sweet spot (30-80% known, no penalty)
    print("\n3. Testing sweet spot (30-80% known, no penalty)...")
    sweet_spot_scores = []
    for known_pct in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
        score = calculate_match_score(
            known_percent=known_pct,
            book_reading_level=7.0,
            student_reading_level=7.0
        )
        sweet_spot_scores.append((known_pct, score))
        print(f"   Known: {known_pct:.0%}, Score: {score:.3f}")
    
    # Check that scores are relatively high in sweet spot
    avg_sweet = sum(s for _, s in sweet_spot_scores) / len(sweet_spot_scores)
    avg_easy = sum(s for _, pct in easy_scores for s in [pct]) / len(easy_scores) if easy_scores else 0
    avg_hard = sum(s for _, pct in hard_scores for s in [pct]) / len(hard_scores) if hard_scores else 0
    
    if avg_sweet > 0.5:
        print(f"   ✅ Average score in sweet spot is good: {avg_sweet:.3f}")
    else:
        print(f"   ⚠️  Average score in sweet spot might be too low: {avg_sweet:.3f}")
        all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL PENALTY LOGIC TESTS PASSED")
    else:
        print("⚠️  SOME TESTS HAD WARNINGS")
    print("=" * 70)
    
    return all_passed


def test_reading_level_bonus():
    """Test reading level bonus application."""
    print("\n" + "=" * 70)
    print("TEST 2.3: Reading Level Bonus")
    print("=" * 70)
    
    all_passed = True
    student_level = 7.0
    
    # Test same reading level (should get highest bonus)
    print("\n1. Testing same reading level...")
    score_same = calculate_match_score(
        known_percent=0.5,
        book_reading_level=7.0,
        student_reading_level=student_level
    )
    print(f"   Book level: 7.0, Student level: {student_level}")
    print(f"   Score: {score_same:.3f}")
    
    # Test ±1 grade (should still be good)
    print("\n2. Testing ±1 grade difference...")
    score_plus1 = calculate_match_score(
        known_percent=0.5,
        book_reading_level=8.0,
        student_reading_level=student_level
    )
    score_minus1 = calculate_match_score(
        known_percent=0.5,
        book_reading_level=6.0,
        student_reading_level=student_level
    )
    print(f"   Book level: 8.0, Score: {score_plus1:.3f}")
    print(f"   Book level: 6.0, Score: {score_minus1:.3f}")
    
    # Test ±2 grades (should be lower)
    print("\n3. Testing ±2 grade difference...")
    score_plus2 = calculate_match_score(
        known_percent=0.5,
        book_reading_level=9.0,
        student_reading_level=student_level
    )
    score_minus2 = calculate_match_score(
        known_percent=0.5,
        book_reading_level=5.0,
        student_reading_level=student_level
    )
    print(f"   Book level: 9.0, Score: {score_plus2:.3f}")
    print(f"   Book level: 5.0, Score: {score_minus2:.3f}")
    
    # Verify that same level >= ±1 >= ±2
    if score_same >= score_plus1 and score_same >= score_minus1:
        print("   ✅ Same level gets highest score")
    else:
        print("   ⚠️  Same level should get highest score")
        all_passed = False
    
    if score_plus1 >= score_plus2 and score_minus1 >= score_minus2:
        print("   ✅ ±1 grade gets better score than ±2 grades")
    else:
        print("   ⚠️  ±1 grade should get better score than ±2")
        all_passed = False
    
    # Test with no reading level
    print("\n4. Testing book with no reading level...")
    score_no_level = calculate_match_score(
        known_percent=0.5,
        book_reading_level=None,
        student_reading_level=student_level
    )
    print(f"   Book level: None, Score: {score_no_level:.3f}")
    if 0 <= score_no_level <= 1:
        print("   ✅ Score is valid (neutral reading level score applied)")
    else:
        print(f"   ❌ Score out of range: {score_no_level:.3f}")
        all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL READING LEVEL BONUS TESTS PASSED")
    else:
        print("⚠️  SOME TESTS HAD WARNINGS")
    print("=" * 70)
    
    return all_passed


def test_edge_cases():
    """Test edge cases."""
    print("\n" + "=" * 70)
    print("TEST 2.4: Edge Cases")
    print("=" * 70)
    
    all_passed = True
    
    # Edge case 1: Student with 0% vocabulary mastery
    print("\n1. Testing student with 0% vocabulary mastery...")
    score = calculate_match_score(
        known_percent=0.0,
        book_reading_level=7.0,
        student_reading_level=7.0
    )
    print(f"   Known: 0%, Score: {score:.3f}")
    if 0 <= score <= 1:
        print("   ✅ Score is valid")
    else:
        print(f"   ❌ Score out of range: {score:.3f}")
        all_passed = False
    
    # Edge case 2: Student with 100% vocabulary mastery
    print("\n2. Testing student with 100% vocabulary mastery...")
    score = calculate_match_score(
        known_percent=1.0,
        book_reading_level=7.0,
        student_reading_level=7.0
    )
    print(f"   Known: 100%, Score: {score:.3f}")
    if 0 <= score <= 1:
        print("   ✅ Score is valid")
        if score < 0.5:
            print("   ✅ Score is penalized (expected for too easy)")
        else:
            print(f"   ⚠️  Score might be too high for 100% known: {score:.3f}")
    else:
        print(f"   ❌ Score out of range: {score:.3f}")
        all_passed = False
    
    # Edge case 3: Book with very low vocabulary coverage
    print("\n3. Testing book with very low vocabulary coverage...")
    # This would be tested with actual book data, but we can test with low known percent
    score = calculate_match_score(
        known_percent=0.05,  # Very few known words
        book_reading_level=7.0,
        student_reading_level=7.0
    )
    print(f"   Known: 5%, Score: {score:.3f}")
    if 0 <= score <= 1:
        print("   ✅ Score is valid")
    else:
        print(f"   ❌ Score out of range: {score:.3f}")
        all_passed = False
    
    # Edge case 4: Book with very high vocabulary coverage
    print("\n4. Testing book with very high vocabulary coverage...")
    score = calculate_match_score(
        known_percent=0.95,  # Almost all words known
        book_reading_level=7.0,
        student_reading_level=7.0
    )
    print(f"   Known: 95%, Score: {score:.3f}")
    if 0 <= score <= 1:
        print("   ✅ Score is valid")
        if score < 0.5:
            print("   ✅ Score is penalized (expected for too easy)")
        else:
            print(f"   ⚠️  Score might be too high for 95% known: {score:.3f}")
    else:
        print(f"   ❌ Score out of range: {score:.3f}")
        all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL EDGE CASE TESTS PASSED")
    else:
        print("⚠️  SOME TESTS HAD WARNINGS")
    print("=" * 70)
    
    return all_passed


def main():
    """Run all algorithm verification tests."""
    print("=" * 70)
    print("ALGORITHM VERIFICATION TESTS")
    print("=" * 70)
    
    results = []
    
    # Run all tests
    results.append(("Match Score Calculation", test_match_score_calculation()))
    results.append(("Penalty Logic", test_penalty_logic()))
    results.append(("Reading Level Bonus", test_reading_level_bonus()))
    results.append(("Edge Cases", test_edge_cases()))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "⚠️  WARNINGS"
        print(f"{test_name}: {status}")
    
    all_passed = all(passed for _, passed in results)
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL ALGORITHM VERIFICATION TESTS PASSED")
    else:
        print("⚠️  SOME TESTS HAD WARNINGS (algorithm may need tuning)")
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

