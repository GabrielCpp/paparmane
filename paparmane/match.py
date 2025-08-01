from llama_cpp import Llama

llm = Llama(
    model_path="./models/mistral-7b-instruct-v0.1.Q5_K_M.gguf",
    # n_gpu_layers=-1, # Uncomment to use GPU acceleration
    seed=1337,  # Uncomment to set a specific seed
    n_ctx=2500,  # Uncomment to increase the context window
    temperature=0.1,
    top_p=0.2,
    top_k=10,
    repeat_penalty=1.2,
    n_threads=4,
)


def check_match(profileA, profileB):
    prompt = f""" 
  ### Instruction
  Assess the compatibility of roommates A and B for intergenerational cohabitation. Allow to match when candidates have any ground. Significant differences are accepted. Answer with `YES` or `NO` in `Output`. In any cases, highligt the key words that lead to the result in the section `Explanation`.
  ### A
  {profileA.to_prompt()}
  ### B 
  {profileB.to_prompt()}
  ### Output

  """
    output = llm(
        prompt,  # Prompt
        echo=False,  # Echo the prompt back in the output
        max_tokens=2500, 
        stop=[], 
    )
    return output

