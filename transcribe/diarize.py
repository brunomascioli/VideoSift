from typing import List, Tuple
from pyannote.core import Segment, Annotation

def extract_text_with_timestamps(transcription_data: dict) -> List[Tuple[Segment, str]]:
    timestamped_text: List[Tuple[Segment, str]] = []
    for entry in transcription_data['segments']:
        start_time: float = entry['start']
        end_time: float = entry['end']
        spoken_text: str = entry['text']
        timestamped_text.append((Segment(start_time, end_time), spoken_text))
    return timestamped_text

def assign_speaker_to_text(timestamped_text: List[Tuple[Segment, str]], diarization_data: Annotation) -> List[Tuple[Segment, str, str]]:
    speaker_text_links: List[Tuple[Segment, str, str]] = []
    for segment, text in timestamped_text:
        assigned_speaker: str = diarization_data.crop(segment).argmax()
        speaker_text_links.append((segment, assigned_speaker, text))
    return speaker_text_links

def combine_segments(segment_data: List[Tuple[Segment, str, str]]) -> Tuple[Segment, str, str]:
    full_text: str = ''.join([part[-1] for part in segment_data])
    speaker_id: str = segment_data[0][1]
    start_time: float = segment_data[0][0].start
    end_time: float = segment_data[-1][0].end
    return Segment(start_time, end_time), speaker_id, full_text

ENDING_PUNCTUATION = ['.', '!', '?']

def consolidate_speaker_text(speaker_text_links: List[Tuple[Segment, str, str]]) -> List[Tuple[Segment, str, str]]:
    combined_texts: List[Tuple[Segment, str, str]] = []
    previous_speaker: str = None
    text_segments: List[Tuple[Segment, str, str]] = []

    for segment, speaker, text in speaker_text_links:
        if speaker != previous_speaker and previous_speaker is not None:
            combined_texts.append(combine_segments(text_segments))
            text_segments = [(segment, speaker, text)]
            previous_speaker = speaker
        elif text and text[-1] in ENDING_PUNCTUATION:
            text_segments.append((segment, speaker, text))
            combined_texts.append(combine_segments(text_segments))
            text_segments = []
            previous_speaker = speaker
        else:
            text_segments.append((segment, speaker, text))
            previous_speaker = speaker

    if text_segments:
        combined_texts.append(combine_segments(text_segments))

    return combined_texts

def process_diarized_text(transcription_data: dict, diarization_data: Annotation) -> List[Tuple[Segment, str, str]]:
    timestamped_text: List[Tuple[Segment, str]] = extract_text_with_timestamps(transcription_data)
    speaker_text_links: List[Tuple[Segment, str, str]] = assign_speaker_to_text(timestamped_text, diarization_data)
    final_output: List[Tuple[Segment, str, str]] = consolidate_speaker_text(speaker_text_links)
    return final_output

def export_to_text_file(final_output: List[Tuple[Segment, str, str]], output_path: str) -> None:
    with open(output_path, 'w') as file:
        for segment, speaker, sentence in final_output:
            line: str = f'{segment.start:.2f} - {segment.end:.2f} | Speaker {speaker}: {sentence}\n'
            file.write(line)
