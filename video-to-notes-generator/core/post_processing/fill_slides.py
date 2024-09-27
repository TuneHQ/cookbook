import os
import re


class SlideReplacer:
    @staticmethod
    def replace_slides(markdown, slides_folder, path) -> str:
        # Rename the slides
        SlideReplacer.rename_slides(slides_folder)

        # Find all instances of [Slide number] and remove backticks if present
        slide_pattern = re.compile(r"`?\[slide (\d+)\]`?")
        matches = slide_pattern.findall(markdown)

        # Get sorted list of images in the slides folder
        images = sorted(
            os.listdir(slides_folder),
            key=lambda x: int(re.findall(r"\d+", x)[0]),
        )

        # Replace each [Slide number] with the corresponding image path
        for match in matches:
            slide_number = int(match)
            if 1 <= slide_number <= len(images):
                image_name = images[slide_number - 1]
                markdown = re.sub(
                    rf"`?\[slide {slide_number}\]`?",
                    f"![Slide {slide_number}]({path}{image_name}#center)",
                    markdown,
                )

        return markdown

    @staticmethod
    def rename_slides(slides_folder) -> None:
        # Sort the files and rename them as slide_1, slide_2, slide_3, ...
        files = os.listdir(slides_folder)
        files.sort(key=lambda x: int(re.findall(r"\d+", x)[0]))
        for i, file in enumerate(files):
            new_name = f"slide_{i + 1}{os.path.splitext(file)[1]}"
            try:
                os.rename(
                    os.path.join(slides_folder, file),
                    os.path.join(slides_folder, new_name),
                )
            except Exception as e:
                print(f"Error renaming file {file}: {e}")


if __name__ == "__main__":
    # testing the function
    markdown = """
    # Lightning Talk: How to Win at Coding Interviews - David Stone - CppCon 2022

    ## Introduction 

    This lightning talk by David Stone at CppCon 2022 presents a "secret protocol" for success in coding interviews. He shares a three-step plan designed to improve your chances of passing technical interviews at large companies. `[Slide 2]`

    ##  Why Listen to Me?

    David Stone has a strong track record of passing technical interviews at major companies, including large tech firms and financial institutions. He believes his experience offers valuable insights into the interview process.

    ## The Three-Step Plan

    ### Repeat the Question `[Slide 4]`

    This crucial first step serves two primary purposes: 
    * **Confirmation**:  It allows you to ensure that you understood the question correctly.
    * **Clarification**: It gives you an opportunity to clarify any ambiguities in the question.

    > "A lot of questions are intentionally ambiguous."

    David emphasizes that this step is vital and should be completed before starting to write code. Skipping it could lead to negative reactions from interviewers who prioritize adherence to their preferred process. 

    ### Write the Interface `[Slide 5]`

    The core of every coding interview solution lies in defining a function that accepts parameters and returns a value. 

    > "The answer to every interview question is going to be a single function that accepts some amount of parameters and returns a value."

    This step involves carefully considering the input and output types required for the problem.

    ### Use a Hash Map `[Slide 6]`

    David advocates for leveraging hash maps as a primary tool for solving coding interview problems. He claims that this approach works effectively in a significant majority of cases. `[Slide 7]`

    > "Only about 85 to 90% of the time does this solve your interview problems."

    He acknowledges that for the remaining cases, mastering algorithms is essential. He recommends studying the algorithms library in C++ reference. 

    ##  Examples

    David demonstrates his method using practical examples from LeetCode. 

    ### Example 1: Majority Element II `[Slide 8]` 

    * **Problem:** Given an integer array of size *n*, find all elements that appear more than *n* over three rounded down times. 
    * **Interface:** `static_vector<int, 2> find_common_elements(std::span<int const> input);` `[Slide 9]`

    The solution involves using a hash map to store the count of each element in the input array. This approach allows for a straightforward and efficient solution. 

    ### Example 2: Two Out of Three `[Slide 10]`

    * **Problem:** Given three integer arrays, *nums1*, *nums2*, and *nums3*, return a distinct array containing all the values that are present in at least two out of the three arrays. You may return the values in any order. 

    > "That last sentence is actually a hint telling you, 'Hey, use a hash map.'"

    This example highlights the importance of reading questions carefully for potential hints. The solution utilizes a struct within a hash map to track the presence of a value in each of the input arrays. 

    ### Example 3: Next Permutation `[Slide 12]`

    * **Problem:** Given an array of integers *nums*, find the next permutation of *nums*.
    * **Solution:** LeetCode classifies this as a "hard" problem. This problem does not lend itself to a straightforward hash map solution and requires the use of a more complex algorithm. 

    > "We have to fall back on our expert-only solution, which is used to algorithm." `[Slide 13]`

    David recommends utilizing the `next_permutation` algorithm from the C++ standard library for this specific problem. 

    ## When Not to Use a Hash Map `[Slide 14]`

    David provides insights into situations where using a hash map may not be the optimal approach:

    * **Sorted Input:**  If the input is already sorted, consider using set-based algorithms.
    * **Specific Order Output:**  If the output needs to be in a specific order, sorting might be necessary. 

    ## Conclusion

    David's talk concludes with a reflection on the nature of coding interviews. 

    > "If we can solve all of the problems this easily, maybe that's a sign that our technical interviews aren't actually testing all of the skills that we need." 

    This comment prompts the audience to ponder the effectiveness of traditional coding interview practices. 

    ## Key Takeaways

    * **Follow the Protocol**: Adhere to the interviewer's preferred process.
    * **Hash Map Power**: Utilize hash maps as a primary problem-solving technique.
    * **Algorithm Mastery**: Study algorithms for more complex cases.
    * **Critical Thinking**:  Analyze the question carefully for hints and consider alternative approaches. 
    * **Beyond Hash Maps**:  Be aware of situations where different algorithms may be more appropriate.
    * **Interview Effectiveness**:  Reflect on the effectiveness of coding interview practices. 
    """
    slides_folder = "test/agile/slides"
    replaced_markdown = SlideReplacer.replace_slides(markdown, slides_folder)
    print(replaced_markdown)
