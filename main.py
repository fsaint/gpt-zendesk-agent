from pygptcalls import gptcall
import zendesk
prompt = "answer open zendesk tickets based on historical answers. Search historical similar tikets by kwyeord as examples on how similat tickets were answered in the past."

print(gptcall(zendesk, prompt))
